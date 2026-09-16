"""
MAVLink hardware backend — full implementation using pymavlink.
Set DRONE_BACKEND=mavlink in environment to activate.

Connection:
    DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py
"""

import math
import threading
import time
import logging

from adapters.base_adapter import BaseAdapter
from adapters.mavlink_cache import MAVLinkCache
from config import (
    MAVLINK_CACHE_MAX_AGE_SEC,
    MAVLINK_ACK_TIMEOUT_SEC,
    MAVLINK_MODE_CONFIRM_SEC,
    MAVLINK_WAIT_ALTITUDE_SEC,
    MAVLINK_WAIT_ARRIVAL_SEC,
)

logger = logging.getLogger(__name__)

# ArduCopter custom mode numbers (ArduPilot firmware)
_ARDUPILOT_MODES = {
    "STABILIZE": 0,
    "ACRO":      1,
    "ALT_HOLD":  2,
    "AUTO":      3,
    "GUIDED":    4,
    "LOITER":    5,
    "RTL":       6,
    "CIRCLE":    7,
    "LAND":      9,
    "POSHOLD":  16,
    "BRAKE":    17,
}
_ARDUPILOT_MODES_INV = {v: k for k, v in _ARDUPILOT_MODES.items()}

# MAVLink integer constants (avoids import at module level — pymavlink may not be installed)
_MAV_CMD_NAV_TAKEOFF           = 22
_MAV_CMD_DO_SET_MODE           = 176
_MAV_CMD_COMPONENT_ARM_DISARM  = 400
_MAV_CMD_CONDITION_YAW         = 115
_MAV_CMD_DO_CHANGE_SPEED       = 178
_MAV_MODE_FLAG_CUSTOM_MODE     = 1     # MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
_MAV_RESULT_ACCEPTED           = 0
_MAV_FRAME_GLOBAL_RELATIVE_ALT_INT = 6     # MAV_FRAME_GLOBAL_RELATIVE_ALT_INT
_HEARTBEAT_WAIT_SEC            = 15.0  # connect_drone's wait_heartbeat budget
# SET_POSITION_TARGET_GLOBAL_INT type_mask: ignore velocity, accel, yaw, yaw_rate; use position only
_POS_TARGET_TYPE_MASK          = 0b110111111000  # bits 3-8, 10-11 ignored; bits 0-2 used

# Telemetry stream IDs (only the three we need)
_STREAMS_TO_REQUEST = [
    (2, "EXTENDED_STATUS (battery, system status)"),      # SYS_STATUS, BATTERY_STATUS
    (6, "POSITION (GPS, altitude, velocity)"),            # GLOBAL_POSITION_INT
    (10, "EXTRA1 (VFR_HUD, attitude)"),                   # VFR_HUD, ATTITUDE
]

# Common error message for telemetry failures
_TELEMETRY_ERROR = "no telemetry received — check: 1) autopilot connected? 2) connected via MAVLink? 3) correct baud rate?"
_NOT_CONNECTED_ERROR = "not connected — call connect_drone first"

# How stale a cached message of each type may be before a read waits for a
# fresh one.  This is a property of the stream's rate, not of the call site:
# HEARTBEAT arrives at 1 Hz, everything else at the 10 Hz requested above.
_STREAM_MAX_AGE = {"HEARTBEAT": 2.0}


class MAVLinkAdapter(BaseAdapter):
    def __init__(self, connection_string: str = "tcp:127.0.0.1:5762"):
        self._connection_string = connection_string
        self._conn = None
        # One reader thread owns the socket; handlers read the cache in O(1)
        # instead of issuing blocking round trips.  See mavlink_cache.py.
        self._cache = None
        # pymavlink sends are not thread-safe and several tasks send
        # concurrently (LLM tool calls, telemetry pollers, workflows).
        self._send_lock = threading.Lock()

    def is_connected(self) -> bool:
        return self._conn is not None

    def disconnect(self):
        if self._cache is not None:
            self._cache.stop()
            self._cache = None
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute(self, tool_name: str, args: dict) -> dict:
        logger.info(f"[MAVLINK] {tool_name}({args})")
        handler = getattr(self, f"_handle_{tool_name}", None)
        if handler is None:
            return {"error": f"MAVLinkAdapter: no handler for '{tool_name}'"}
        # Single connection gate for every handler but connect_drone itself.
        # An unhandled AttributeError on a None connection would cost the
        # dispatcher a retry and an extra LLM round trip.
        if tool_name != "connect_drone" and self._cache is None:
            return {"error": _NOT_CONNECTED_ERROR}
        return handler(**args)

    def timeout_for(self, tool_name: str, args: dict) -> float:
        """
        Execution deadline for one tool call, in seconds.

        These are properties of THIS backend, not of the tool: only the code
        that does the waiting knows how long its wait can legitimately take.
        SimAdapter returns instantly and keeps the base default.
        """
        if tool_name == "connect_drone":
            return _HEARTBEAT_WAIT_SEC + 5.0
        if tool_name == "wait_altitude":
            return MAVLINK_WAIT_ALTITUDE_SEC + 5.0
        if tool_name == "wait_arrival":
            return MAVLINK_WAIT_ARRIVAL_SEC + 5.0
        if tool_name == "wait_time":
            # _handle_wait_time actually sleeps here; SimAdapter returns at once.
            try:
                return float(args.get("seconds", 0.0)) + 5.0
            except (TypeError, ValueError):
                pass
        return super().timeout_for(tool_name, args)

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _recv(self, msg_type: str, timeout: float = 5.0):
        """
        Latest message of this type — the one read idiom in this file.

        A cache hit (the common case on a live stream) costs microseconds; the
        blocking read this replaced cost 100 ms-5 s and threw away every other
        consumer's messages while it waited.  ``timeout=0`` checks the cache
        once and never blocks.
        """
        if self._cache is None:
            return None
        return self._cache.wait(
            msg_type,
            timeout=timeout,
            max_age=_STREAM_MAX_AGE.get(msg_type, MAVLINK_CACHE_MAX_AGE_SEC),
        )

    def _request_streams(self):
        """Request all required telemetry streams from autopilot."""
        try:
            for stream_id, description in _STREAMS_TO_REQUEST:
                self._conn.mav.request_data_stream_send(
                    self._conn.target_system,
                    self._conn.target_component,
                    stream_id,
                    10,  # 10 Hz
                    1,   # start
                )
            logger.info("[MAVLINK] Requested telemetry streams")
        except Exception as e:
            logger.warning(f"[MAVLINK] Could not request streams (non-fatal): {e}")

    def _prime_cache(self, timeout: float = 3.0) -> None:
        """
        Wait for the reader thread to see the first heartbeat + position so the
        first telemetry tool call is a cache hit rather than a cold wait.
        Replaces the old fixed 0.3 s drain-and-sleep.

        Both types share one deadline — the reader fills them concurrently, so
        waiting on them serially would only ever add up their timeouts on a
        degraded link.
        """
        if self._cache is None:
            return
        deadline = time.monotonic() + timeout
        for msg_type in ("HEARTBEAT", "GLOBAL_POSITION_INT"):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            self._cache.wait(msg_type, timeout=remaining)
        logger.info(f"[MAVLINK] Cache primed: {self._cache.stats()}")

    def _send_command_long(self, command: int, p1=0.0, p2=0.0, p3=0.0,
                           p4=0.0, p5=0.0, p6=0.0, p7=0.0,
                           ack_timeout: float = MAVLINK_ACK_TIMEOUT_SEC):
        """
        Send COMMAND_LONG and wait for COMMAND_ACK.
        Returns (True, "ok") on MAV_RESULT_ACCEPTED, (False, reason) otherwise.
        """
        sent_at = time.monotonic()
        with self._send_lock:
            self._conn.mav.command_long_send(
                self._conn.target_system,
                self._conn.target_component,
                command, 0,
                float(p1), float(p2), float(p3), float(p4),
                float(p5), float(p6), float(p7),
            )
        # Match the ACK to THIS command id and to a timestamp after the send,
        # so a stale ACK for another command can never satisfy this wait.
        ack = self._cache.wait_ack(command, since=sent_at, timeout=ack_timeout)
        if ack is None:
            return False, "no COMMAND_ACK received"
        if ack.result != _MAV_RESULT_ACCEPTED:
            return False, f"rejected (result={ack.result})"
        return True, "ok"

    @staticmethod
    def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6_371_000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi    = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = (math.sin(dphi / 2) ** 2
             + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # ── Handlers ─────────────────────────────────────────────────────────────

    def _handle_connect_drone(self, connection_string=None):
        from pymavlink import mavutil
        uri = connection_string or self._connection_string
        try:
            self._conn = mavutil.mavlink_connection(uri)
            self._conn.wait_heartbeat(timeout=_HEARTBEAT_WAIT_SEC)
            logger.info(
                f"[MAVLINK] Connected — system={self._conn.target_system} "
                f"component={self._conn.target_component}"
            )
            self._request_streams()
            self._cache = MAVLinkCache(
                self._conn, source_system=self._conn.target_system
            )
            self._cache.start()
            self._prime_cache()
            return {"status": "connected", "connection_string": uri}
        except Exception as exc:
            self._conn = None
            return {"error": f"connect failed: {exc}"}

    def _handle_get_current_state(self):
        # HEARTBEAT is a 1 Hz stream — a sub-2 s cached copy is always current
        # enough, and avoids blocking up to a full heartbeat period.
        msg = self._recv("HEARTBEAT", timeout=2.0)
        if msg is None:
            return {"error": "no HEARTBEAT received"}
        armed = bool(msg.base_mode & 0x80)  # MAV_MODE_FLAG_SAFETY_ARMED = 128
        mode_str = _ARDUPILOT_MODES_INV.get(msg.custom_mode, f"MODE_{msg.custom_mode}")
        _sys_status = {
            0: "UNINIT", 1: "BOOT", 2: "CALIBRATING", 3: "STANDBY",
            4: "ACTIVE", 5: "CRITICAL", 6: "EMERGENCY", 7: "POWEROFF",
        }
        system_status = _sys_status.get(msg.system_status, "UNKNOWN")
        return {"mode": mode_str, "armed": armed, "system_status": system_status}

    def _handle_get_telemetry(self):
        pos = self._recv("GLOBAL_POSITION_INT", timeout=5.0)
        if pos is None:
            return {"error": _TELEMETRY_ERROR}
        
        vfr = self._recv("VFR_HUD", timeout=0.0)
        altitude    = pos.relative_alt / 1000.0
        heading     = pos.hdg / 100.0 if pos.hdg != 65535 else 0.0
        airspeed    = vfr.airspeed    if vfr else 0.0
        groundspeed = (vfr.groundspeed if vfr
                       else math.sqrt((pos.vx / 100.0) ** 2 + (pos.vy / 100.0) ** 2))
        return {
            "altitude":    round(altitude, 2),
            "airspeed":    round(airspeed, 2),
            "groundspeed": round(groundspeed, 2),
            "heading":     round(heading, 1),
        }

    def _handle_get_position_str(self):
        pos = self._recv("GLOBAL_POSITION_INT", timeout=5.0)
        if pos is None:
            return {"error": _TELEMETRY_ERROR}
        lat = pos.lat / 1e7
        lon = pos.lon / 1e7
        alt = pos.relative_alt / 1000.0
        return {"position": f"Lat: {lat:.6f}, Lon: {lon:.6f}, Alt: {alt:.1f}m"}

    def _handle_get_battery(self):
        # Prefer BATTERY_STATUS (richer); fall back to SYS_STATUS
        msg = self._recv("BATTERY_STATUS", timeout=3.0)
        if msg is not None:
            voltage = msg.voltages[0] / 1000.0 if msg.voltages[0] != 65535 else 0.0
            current = msg.current_battery / 100.0
            level   = float(msg.battery_remaining)
        else:
            msg = self._recv("SYS_STATUS", timeout=3.0)
            if msg is None:
                return {"error": _TELEMETRY_ERROR}
            voltage = msg.voltage_battery / 1000.0
            current = msg.current_battery / 100.0
            level   = float(msg.battery_remaining)

        # battery_remaining == -1 means "unknown"; estimate from voltage (3S LiPo range)
        if level < 0:
            level = min(100.0, max(0.0, (voltage - 10.0) / (12.6 - 10.0) * 100.0))

        return {
            "voltage":       round(voltage, 2),
            "current":       round(current, 2),
            "level_percent": round(level, 1),   # safety_policy reads this exact key
        }

    def _handle_get_distance_to_str(self, target_lat: float, target_lon: float):
        pos = self._recv("GLOBAL_POSITION_INT")
        if pos is None:
            return {"error": "no position data"}
        lat = pos.lat / 1e7
        lon = pos.lon / 1e7
        dist    = self._haversine_m(lat, lon, target_lat, target_lon)
        dlat    = (target_lat - lat) * 111_000
        dlon    = (target_lon - lon) * 111_000 * math.cos(math.radians(lat))
        bearing = math.degrees(math.atan2(dlon, dlat)) % 360
        return {"distance_str": f"{dist:.1f} meters", "bearing": round(bearing, 1)}

    def _handle_set_mode(self, mode: str):
        mode_id = _ARDUPILOT_MODES.get(mode.upper())
        if mode_id is None:
            return {"error": f"unknown mode '{mode}'; valid: {sorted(_ARDUPILOT_MODES)}"}

        # Fast path — already in the requested mode.  goto_position / takeoff /
        # land all route through here, and after takeoff the vehicle is already
        # in GUIDED, so this turns a ~1 s heartbeat wait into a cache read.
        hb = self._recv("HEARTBEAT", timeout=2.0)
        if hb is not None and hb.custom_mode == mode_id:
            return {"status": "ok", "mode": mode.upper()}

        with self._send_lock:
            self._conn.mav.command_long_send(
                self._conn.target_system,
                self._conn.target_component,
                _MAV_CMD_DO_SET_MODE, 0,
                float(_MAV_MODE_FLAG_CUSTOM_MODE),
                float(mode_id),
                0.0, 0.0, 0.0, 0.0, 0.0,
            )
        # Confirm against the cached HEARTBEAT stream.  Polling the cache
        # cannot swallow messages other handlers are waiting for.
        hb = self._cache.wait(
            "HEARTBEAT",
            timeout=MAVLINK_MODE_CONFIRM_SEC,
            match=lambda m: m.custom_mode == mode_id,
        ) if self._cache else None
        if hb is not None:
            return {"status": "ok", "mode": mode.upper()}
        return {
            "error": f"mode change to '{mode}' not confirmed within "
                     f"{MAVLINK_MODE_CONFIRM_SEC} s"
        }

    def _handle_arm_drone(self):
        ok, reason = self._send_command_long(_MAV_CMD_COMPONENT_ARM_DISARM, p1=1)
        if not ok:
            return {"error": f"arm failed: {reason}"}
        return {"status": "armed"}

    def _handle_disarm_drone(self):
        ok, reason = self._send_command_long(_MAV_CMD_COMPONENT_ARM_DISARM, p1=0)
        if not ok:
            return {"error": f"disarm failed: {reason}"}
        return {"status": "disarmed"}

    def _handle_takeoff(self, altitude: float):
        # Takeoff requires GUIDED mode
        mode_res = self._handle_set_mode("GUIDED")
        if "error" in mode_res:
            return mode_res
        ok, reason = self._send_command_long(
            _MAV_CMD_NAV_TAKEOFF,
            p1=0, p2=0, p3=0, p4=0,  # pitch, empty, empty, yaw (0 = current)
            p5=0, p6=0,               # lat/lon (0 = current)
            p7=altitude,
        )
        if not ok:
            return {"error": f"takeoff failed: {reason}"}
        return {"status": "taking_off", "target_altitude": altitude}

    def _handle_land(self):
        result = self._handle_set_mode("LAND")
        if "error" in result:
            return result
        return {"status": "landing"}

    def _handle_return_to_launch(self):
        result = self._handle_set_mode("RTL")
        if "error" in result:
            return result
        return {"status": "returning_to_launch"}

    def _handle_goto_position(self, lat: float, lon: float, alt: float):
        mode_res = self._handle_set_mode("GUIDED")
        if "error" in mode_res:
            return mode_res
        with self._send_lock:
            self._conn.mav.set_position_target_global_int_send(
                0,                                      # time_boot_ms (ignored)
                self._conn.target_system,
                self._conn.target_component,
                _MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
                _POS_TARGET_TYPE_MASK,
                int(lat * 1e7),                         # lat_int
                int(lon * 1e7),                         # lon_int
                alt,                                    # alt (metres, relative)
                0.0, 0.0, 0.0,                          # vx, vy, vz  (ignored)
                0.0, 0.0, 0.0,                          # ax, ay, az  (ignored)
                0.0, 0.0,                               # yaw, yaw_rate (ignored)
            )
        return {"status": "moving", "target": {"lat": lat, "lon": lon, "alt": alt}}

    def _handle_set_yaw(self, yaw_deg: float, relative: bool = False):
        ok, reason = self._send_command_long(
            _MAV_CMD_CONDITION_YAW,
            p1=yaw_deg,              # target angle (deg)
            p2=10.0,                 # angular speed (deg/s)
            p3=1.0,                  # direction: 1 = CW, -1 = CCW
            p4=1.0 if relative else 0.0,
        )
        if not ok:
            return {"error": f"set_yaw failed: {reason}"}
        return {"status": "ok", "yaw_deg": yaw_deg}

    def _handle_set_speed(self, speed_ms: float):
        ok, reason = self._send_command_long(
            _MAV_CMD_DO_CHANGE_SPEED,
            p1=1.0,       # speed type: 1 = groundspeed
            p2=speed_ms,
            p3=-1.0,      # throttle: -1 = no change
        )
        if not ok:
            return {"error": f"set_speed failed: {reason}"}
        return {"status": "ok", "speed_ms": speed_ms}

    def _handle_wait_altitude(self, target_alt: float, tolerance: float = 0.5,
                              timeout: float = MAVLINK_WAIT_ALTITUDE_SEC):
        """
        Poll the cached position stream at 20 Hz.  The old loop did a 2 s
        blocking recv plus a 0.2 s sleep per iteration, so it detected arrival
        up to ~2.2 s late and consumed messages other handlers needed.
        """
        pos = self._cache.wait(
            "GLOBAL_POSITION_INT",
            timeout=timeout,
            max_age=MAVLINK_CACHE_MAX_AGE_SEC,
            match=lambda p: abs(p.relative_alt / 1000.0 - target_alt) <= tolerance,
        )
        if pos is None:
            return {"error": f"timed out waiting for altitude {target_alt} m"}
        return {"status": "altitude_reached", "altitude": round(pos.relative_alt / 1000.0, 2)}

    def _handle_wait_arrival(self, tolerance_m: float = 1.0,
                             timeout: float = MAVLINK_WAIT_ARRIVAL_SEC):
        """
        Arrived = groundspeed below 0.5 m/s for 3 consecutive fresh samples.
        Reads the cached VFR_HUD stream, so "consecutive" now means three
        distinct messages rather than three blocking round trips.
        """
        deadline  = time.monotonic() + timeout
        stable    = 0
        last_seen = None
        while time.monotonic() < deadline:
            vfr, stamp = self._cache.get_with_ts(
                "VFR_HUD", max_age=MAVLINK_CACHE_MAX_AGE_SEC
            )
            if vfr is None:
                stable = 0
            elif stamp != last_seen:            # count new samples only
                last_seen = stamp
                if vfr.groundspeed < 0.5:
                    stable += 1
                    if stable >= 3:
                        return {"status": "arrived"}
                else:
                    stable = 0
            time.sleep(0.05)
        return {"error": "timed out waiting for arrival"}

    def _handle_wait_time(self, seconds: float):
        time.sleep(seconds)
        return {"status": "done", "waited_seconds": seconds}
