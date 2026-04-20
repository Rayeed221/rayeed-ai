"""
MAVLink hardware backend — full implementation using pymavlink.
Set DRONE_BACKEND=mavlink in environment to activate.

Connection:
    DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py

Architecture:
    A single background reader thread owns the pymavlink connection. It requests
    MAV_DATA_STREAM_ALL at STREAM_RATE_HZ and routes each received message into
    self._snapshot (a thread-safe dict). All _handle_* methods read from this
    snapshot — they never call recv_match themselves, which eliminates the
    concurrent-reader race on the underlying socket.

    Command-sending handlers (arm, takeoff, set_mode, goto_position, …) write to
    the link via self._conn.mav.* and then observe the snapshot to confirm.
"""

import math
import time
import threading
import logging

from adapters.base_adapter import BaseAdapter

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

_SYS_STATUS_NAMES = {
    0: "UNINIT", 1: "BOOT", 2: "CALIBRATING", 3: "STANDBY",
    4: "ACTIVE", 5: "CRITICAL", 6: "EMERGENCY", 7: "POWEROFF",
}

# MAVLink integer constants
_MAV_CMD_NAV_TAKEOFF           = 22
_MAV_CMD_DO_SET_MODE           = 176
_MAV_CMD_COMPONENT_ARM_DISARM  = 400
_MAV_CMD_CONDITION_YAW         = 115
_MAV_CMD_DO_CHANGE_SPEED       = 178
_MAV_MODE_FLAG_CUSTOM_MODE     = 1
_MAV_RESULT_ACCEPTED           = 0
_POS_TARGET_TYPE_MASK          = 0b110111111000

# ESTIMATOR_STATUS flag bits — "healthy" means attitude + horiz-velocity + abs-pos valid
_EKF_HEALTHY_MASK = 0x01 | 0x02 | 0x10   # ATTITUDE | VEL_HORIZ | POS_HORIZ_ABS

STREAM_RATE_HZ    = 50
_ACK_TIMEOUT_S    = 10.0
_CONFIRM_TIMEOUT_S = 5.0


class MAVLinkAdapter(BaseAdapter):
    def __init__(self, connection_string: str = "udp:127.0.0.1:14550"):
        self._connection_string = connection_string
        self._conn = None

        self._snapshot:      dict              = {}
        self._snapshot_lock: threading.Lock    = threading.Lock()
        self._reader_thread: threading.Thread  = None
        self._stop_reader:   threading.Event   = threading.Event()
        self._send_lock:     threading.Lock    = threading.Lock()

    # ── Public adapter interface ─────────────────────────────────────────────

    def is_connected(self) -> bool:
        return self._conn is not None

    def disconnect(self):
        self._stop_stream()
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

    def execute(self, tool_name: str, args: dict) -> dict:
        logger.info(f"[MAVLINK] {tool_name}({args})")
        handler = getattr(self, f"_handle_{tool_name}", None)
        if handler is None:
            return {"error": f"MAVLinkAdapter: no handler for '{tool_name}'"}
        return handler(**args)

    def snapshot(self) -> dict:
        with self._snapshot_lock:
            return dict(self._snapshot)

    # ── Stream reader ────────────────────────────────────────────────────────

    def _start_stream(self, rate_hz: int = STREAM_RATE_HZ):
        if self._reader_thread and self._reader_thread.is_alive():
            return
        try:
            self._conn.mav.request_data_stream_send(
                self._conn.target_system,
                self._conn.target_component,
                _mav_data_stream_all(),
                rate_hz, 1,
            )
        except Exception as exc:
            logger.warning(f"[MAVLINK] Could not request data stream: {exc}")

        self._stop_reader.clear()
        self._reader_thread = threading.Thread(
            target=self._stream_loop, name="mavlink-reader", daemon=True,
        )
        self._reader_thread.start()
        logger.info(f"[MAVLINK] Stream reader started @ {rate_hz} Hz")

    def _stop_stream(self):
        self._stop_reader.set()
        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=1.0)
        self._reader_thread = None

    def _stream_loop(self):
        while not self._stop_reader.is_set():
            try:
                msg = self._conn.recv_match(blocking=True, timeout=0.2)
            except Exception as exc:
                logger.warning(f"[MAVLINK] recv_match error: {exc}")
                time.sleep(0.1)
                continue
            if msg is None:
                continue
            try:
                self._route_msg(msg)
            except Exception as exc:
                logger.debug(f"[MAVLINK] route error for {msg.get_type()}: {exc}")

    def _route_msg(self, msg):
        t = msg.get_type()
        with self._snapshot_lock:
            self._snapshot["timestamp"] = time.time()

            if t == "HEARTBEAT":
                self._snapshot["armed"] = bool(msg.base_mode & 0x80)
                self._snapshot["mode"] = _ARDUPILOT_MODES_INV.get(
                    msg.custom_mode, f"MODE_{msg.custom_mode}"
                )
                self._snapshot["system_status"] = _SYS_STATUS_NAMES.get(
                    msg.system_status, "UNKNOWN"
                )

            elif t == "GLOBAL_POSITION_INT":
                self._snapshot["lat"]      = msg.lat / 1e7
                self._snapshot["lon"]      = msg.lon / 1e7
                self._snapshot["altitude"] = round(msg.relative_alt / 1000.0, 2)
                self._snapshot["heading"]  = (
                    round(msg.hdg / 100.0, 1) if msg.hdg != 65535 else 0.0
                )

            elif t == "VFR_HUD":
                self._snapshot["airspeed"]    = round(msg.airspeed, 2)
                self._snapshot["groundspeed"] = round(msg.groundspeed, 2)

            elif t == "BATTERY_STATUS":
                voltage = msg.voltages[0] / 1000.0 if msg.voltages and msg.voltages[0] != 65535 else 0.0
                current = msg.current_battery / 100.0
                level   = float(msg.battery_remaining)
                if level < 0:  # -1 = unknown → estimate from voltage (3S LiPo)
                    level = min(100.0, max(0.0, (voltage - 10.0) / (12.6 - 10.0) * 100.0))
                self._snapshot["voltage"]     = round(voltage, 2)
                self._snapshot["current"]     = round(current, 2)
                self._snapshot["battery_pct"] = round(level, 1)

            elif t == "SYS_STATUS" and "battery_pct" not in self._snapshot:
                voltage = msg.voltage_battery / 1000.0
                current = msg.current_battery / 100.0
                level   = float(msg.battery_remaining)
                if level < 0:
                    level = min(100.0, max(0.0, (voltage - 10.0) / (12.6 - 10.0) * 100.0))
                self._snapshot["voltage"]     = round(voltage, 2)
                self._snapshot["current"]     = round(current, 2)
                self._snapshot["battery_pct"] = round(level, 1)

            elif t == "HOME_POSITION":
                self._snapshot["home_lat"] = msg.latitude / 1e7
                self._snapshot["home_lon"] = msg.longitude / 1e7
                self._snapshot["home_set"] = True

            elif t == "EXTENDED_SYS_STATE":
                # MAV_LANDED_STATE: 0=undefined, 1=on_ground, 2=in_air, 3=takeoff, 4=landing
                self._snapshot["landed_state"] = int(msg.landed_state)

            elif t == "ESTIMATOR_STATUS":
                self._snapshot["ekf_ok"] = (int(msg.flags) & _EKF_HEALTHY_MASK) == _EKF_HEALTHY_MASK

            elif t == "NAV_CONTROLLER_OUTPUT":
                self._snapshot["wp_dist"] = float(msg.wp_dist)

            elif t == "COMMAND_ACK":
                acks = self._snapshot.setdefault("acks", {})
                acks[int(msg.command)] = {
                    "result": int(msg.result),
                    "time":   time.time(),
                }

    def _wait_snapshot(self, key: str, timeout: float = 3.0):
        """Block until `key` appears in snapshot or timeout expires. Returns value or None."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._snapshot_lock:
                if key in self._snapshot:
                    return self._snapshot[key]
            time.sleep(0.05)
        return None

    # ── Send helpers ─────────────────────────────────────────────────────────

    def _send_command_long(self, command: int, p1=0.0, p2=0.0, p3=0.0,
                           p4=0.0, p5=0.0, p6=0.0, p7=0.0,
                           ack_timeout: float = _ACK_TIMEOUT_S):
        """
        Send COMMAND_LONG and await its ACK. COMMAND_ACKs are collected by the
        reader thread into snapshot["acks"][command_id].
        """
        # Clear any stale ack for this command before sending
        with self._snapshot_lock:
            self._snapshot.get("acks", {}).pop(command, None)
        with self._send_lock:
            self._conn.mav.command_long_send(
                self._conn.target_system,
                self._conn.target_component,
                command, 0,
                float(p1), float(p2), float(p3), float(p4),
                float(p5), float(p6), float(p7),
            )
        return self._await_ack(command, timeout=ack_timeout)

    def _await_ack(self, command: int, timeout: float):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._snapshot_lock:
                ack = self._snapshot.get("acks", {}).get(command)
            if ack:
                if ack["result"] == _MAV_RESULT_ACCEPTED:
                    return True, "ok"
                return False, f"rejected (result={ack['result']})"
            time.sleep(0.05)
        return False, "no COMMAND_ACK received"

    @staticmethod
    def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6_371_000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi    = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = (math.sin(dphi / 2) ** 2
             + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # ── Handlers (read paths — all served from snapshot) ─────────────────────

    def _handle_connect_drone(self, connection_string=None):
        from pymavlink import mavutil
        uri = connection_string or self._connection_string
        try:
            self._conn = mavutil.mavlink_connection(uri)
            self._conn.wait_heartbeat(timeout=15)
            logger.info(
                f"[MAVLINK] heartbeat from system={self._conn.target_system} "
                f"component={self._conn.target_component}"
            )
            self._start_stream()
            return {"status": "connected", "connection_string": uri}
        except Exception as exc:
            self._conn = None
            return {"error": f"connect failed: {exc}"}

    def _handle_get_current_state(self):
        snap = self.snapshot()
        if "mode" not in snap:
            return {"error": "no HEARTBEAT in snapshot yet"}
        return {
            "mode":          snap["mode"],
            "armed":         snap.get("armed", False),
            "system_status": snap.get("system_status", "UNKNOWN"),
        }

    def _handle_get_telemetry(self):
        snap = self.snapshot()
        if "altitude" not in snap:
            return {"error": "no GLOBAL_POSITION_INT in snapshot yet"}
        return {
            "altitude":    snap.get("altitude", 0.0),
            "airspeed":    snap.get("airspeed", 0.0),
            "groundspeed": snap.get("groundspeed", 0.0),
            "heading":     snap.get("heading", 0.0),
        }

    def _handle_get_position_str(self):
        snap = self.snapshot()
        if "lat" not in snap:
            return {"error": "no position in snapshot yet"}
        return {
            "position": (
                f"Lat: {snap['lat']:.6f}, Lon: {snap['lon']:.6f}, "
                f"Alt: {snap.get('altitude', 0.0):.1f}m"
            )
        }

    def _handle_get_battery(self):
        snap = self.snapshot()
        if "battery_pct" not in snap:
            return {"error": "no BATTERY_STATUS in snapshot yet"}
        return {
            "voltage":       snap.get("voltage", 0.0),
            "current":       snap.get("current", 0.0),
            "level_percent": snap["battery_pct"],   # safety_policy reads this key
        }

    def _handle_get_distance_to_str(self, target_lat: float, target_lon: float):
        snap = self.snapshot()
        if "lat" not in snap:
            return {"error": "no position in snapshot yet"}
        lat, lon = snap["lat"], snap["lon"]
        dist    = self._haversine_m(lat, lon, target_lat, target_lon)
        dlat    = (target_lat - lat) * 111_000
        dlon    = (target_lon - lon) * 111_000 * math.cos(math.radians(lat))
        bearing = math.degrees(math.atan2(dlon, dlat)) % 360
        return {"distance_str": f"{dist:.1f} meters", "bearing": round(bearing, 1)}

    def _handle_get_status(self):
        return self.snapshot()

    # ── Handlers (write paths — send command, confirm via snapshot) ──────────

    def _handle_set_mode(self, mode: str):
        mode_id = _ARDUPILOT_MODES.get(mode.upper())
        if mode_id is None:
            return {"error": f"unknown mode '{mode}'; valid: {sorted(_ARDUPILOT_MODES)}"}
        with self._send_lock:
            self._conn.mav.command_long_send(
                self._conn.target_system,
                self._conn.target_component,
                _MAV_CMD_DO_SET_MODE, 0,
                float(_MAV_MODE_FLAG_CUSTOM_MODE),
                float(mode_id),
                0.0, 0.0, 0.0, 0.0, 0.0,
            )
        # Confirm by watching snapshot["mode"]
        deadline = time.monotonic() + _CONFIRM_TIMEOUT_S
        target = mode.upper()
        while time.monotonic() < deadline:
            if self.snapshot().get("mode") == target:
                return {"status": "ok", "mode": target}
            time.sleep(0.1)
        return {"error": f"mode change to '{mode}' not confirmed within {_CONFIRM_TIMEOUT_S}s"}

    def _handle_arm_drone(self):
        ok, reason = self._send_command_long(_MAV_CMD_COMPONENT_ARM_DISARM, p1=1)
        if not ok:
            return {"error": f"arm failed: {reason}"}
        # Confirm via snapshot
        deadline = time.monotonic() + _CONFIRM_TIMEOUT_S
        while time.monotonic() < deadline:
            if self.snapshot().get("armed") is True:
                return {"status": "armed"}
            time.sleep(0.1)
        return {"error": "arm command ACKed but armed flag not observed"}

    def _handle_disarm_drone(self):
        ok, reason = self._send_command_long(_MAV_CMD_COMPONENT_ARM_DISARM, p1=0)
        if not ok:
            return {"error": f"disarm failed: {reason}"}
        deadline = time.monotonic() + _CONFIRM_TIMEOUT_S
        while time.monotonic() < deadline:
            if self.snapshot().get("armed") is False:
                return {"status": "disarmed"}
            time.sleep(0.1)
        return {"error": "disarm command ACKed but armed flag still set"}

    def _handle_takeoff(self, altitude: float):
        mode_res = self._handle_set_mode("GUIDED")
        if "error" in mode_res:
            return mode_res
        ok, reason = self._send_command_long(
            _MAV_CMD_NAV_TAKEOFF,
            p1=0, p2=0, p3=0, p4=0, p5=0, p6=0, p7=altitude,
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
        from pymavlink import mavutil
        mode_res = self._handle_set_mode("GUIDED")
        if "error" in mode_res:
            return mode_res
        with self._send_lock:
            self._conn.mav.set_position_target_global_int_send(
                0,
                self._conn.target_system,
                self._conn.target_component,
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
                _POS_TARGET_TYPE_MASK,
                int(lat * 1e7),
                int(lon * 1e7),
                alt,
                0.0, 0.0, 0.0,
                0.0, 0.0, 0.0,
                0.0, 0.0,
            )
        return {"status": "moving", "target": {"lat": lat, "lon": lon, "alt": alt}}

    def _handle_set_yaw(self, yaw_deg: float, relative: bool = False):
        ok, reason = self._send_command_long(
            _MAV_CMD_CONDITION_YAW,
            p1=yaw_deg, p2=10.0, p3=1.0,
            p4=1.0 if relative else 0.0,
        )
        if not ok:
            return {"error": f"set_yaw failed: {reason}"}
        return {"status": "ok", "yaw_deg": yaw_deg}

    def _handle_set_speed(self, speed_ms: float):
        ok, reason = self._send_command_long(
            _MAV_CMD_DO_CHANGE_SPEED,
            p1=1.0, p2=speed_ms, p3=-1.0,
        )
        if not ok:
            return {"error": f"set_speed failed: {reason}"}
        return {"status": "ok", "speed_ms": speed_ms}

    def _handle_wait_altitude(self, target_alt: float, tolerance: float = 0.5):
        deadline = time.monotonic() + 60.0
        while time.monotonic() < deadline:
            current = self.snapshot().get("altitude")
            if current is not None and abs(current - target_alt) <= tolerance:
                return {"status": "altitude_reached", "altitude": round(current, 2)}
            time.sleep(0.1)
        return {"error": f"timed out waiting for altitude {target_alt} m"}

    def _handle_wait_arrival(self, tolerance_m: float = 1.0):
        """
        Prefer NAV_CONTROLLER_OUTPUT.wp_dist (exact) with a groundspeed fallback.
        """
        deadline = time.monotonic() + 120.0
        stable_slow = 0
        while time.monotonic() < deadline:
            snap = self.snapshot()
            if "wp_dist" in snap and snap["wp_dist"] <= tolerance_m:
                return {"status": "arrived", "wp_dist": snap["wp_dist"]}
            if snap.get("groundspeed", 999.0) < 0.5:
                stable_slow += 1
                if stable_slow >= 15:  # ~1.5 s at 100 ms cadence
                    return {"status": "arrived"}
            else:
                stable_slow = 0
            time.sleep(0.1)
        return {"error": "timed out waiting for arrival"}

    def _handle_wait_time(self, seconds: float):
        time.sleep(seconds)
        return {"status": "done", "waited_seconds": seconds}


# Deferred import: pymavlink may not be installed when module is imported
def _mav_data_stream_all():
    from pymavlink import mavutil
    return mavutil.mavlink.MAV_DATA_STREAM_ALL
