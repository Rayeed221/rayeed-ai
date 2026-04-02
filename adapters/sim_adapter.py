import math
import logging

from adapters.base_adapter import BaseAdapter

logger = logging.getLogger(__name__)


class SimAdapter(BaseAdapter):
    """
    Simulated drone backend — no hardware required.
    Maintains internal state to produce realistic-looking responses.
    All tool names map to _handle_<tool_name>() methods.
    """

    def __init__(self):
        self._connected   = False
        self._armed       = False
        self._mode        = "STABILIZE"
        self._altitude    = 0.0
        self._lat         = 23.8103
        self._lon         = 90.4125
        self._heading     = 0.0
        self._speed       = 5.0
        self._battery_pct = 95.0

    def is_connected(self) -> bool:
        return self._connected

    def disconnect(self):
        self._connected = False

    def execute(self, tool_name: str, args: dict) -> dict:
        logger.info(f"[SIM] {tool_name}({args})")
        handler = getattr(self, f"_handle_{tool_name}", None)
        if handler is None:
            return {"error": f"SimAdapter: no handler for '{tool_name}'"}
        return handler(**args)

    # ── Handlers ─────────────────────────────────────────────────────────────

    def _handle_connect_drone(self, connection_string="udp:127.0.0.1:14550"):
        self._connected = True
        return {"status": "connected", "connection_string": connection_string}

    def _handle_get_current_state(self):
        return {
            "mode": self._mode,
            "armed": self._armed,
            "system_status": "ACTIVE" if self._connected else "STANDBY",
        }

    def _handle_get_telemetry(self):
        return {
            "altitude":    self._altitude,
            "airspeed":    self._speed,
            "groundspeed": self._speed,
            "heading":     self._heading,
        }

    def _handle_get_position_str(self):
        return {
            "position": f"Lat: {self._lat:.6f}, Lon: {self._lon:.6f}, Alt: {self._altitude:.1f}m"
        }

    def _handle_get_battery(self):
        self._battery_pct = max(0.0, self._battery_pct - 0.05)
        return {"voltage": 12.4, "current": 0.5, "level_percent": round(self._battery_pct, 2)}

    def _handle_get_distance_to_str(self, target_lat: float, target_lon: float):
        dlat = (target_lat - self._lat) * 111000
        dlon = (target_lon - self._lon) * 111000 * math.cos(math.radians(self._lat))
        dist = math.sqrt(dlat ** 2 + dlon ** 2)
        bearing = math.degrees(math.atan2(dlon, dlat)) % 360
        return {"distance_str": f"{dist:.1f} meters", "bearing": round(bearing, 1)}

    def _handle_set_mode(self, mode: str):
        self._mode = mode
        return {"status": "ok", "mode": mode}

    def _handle_arm_drone(self):
        self._armed = True
        return {"status": "armed"}

    def _handle_disarm_drone(self):
        self._armed = False
        return {"status": "disarmed"}

    def _handle_takeoff(self, altitude: float):
        self._altitude = altitude
        return {"status": "taking_off", "target_altitude": altitude}

    def _handle_land(self):
        self._altitude = 0.0
        self._armed    = False
        return {"status": "landing"}

    def _handle_return_to_launch(self):
        self._lat = 23.8103
        self._lon = 90.4125
        return {"status": "returning_to_launch"}

    def _handle_goto_position(self, lat: float, lon: float, alt: float):
        self._lat      = lat
        self._lon      = lon
        self._altitude = alt
        return {"status": "moving", "target": {"lat": lat, "lon": lon, "alt": alt}}

    def _handle_set_yaw(self, yaw_deg: float, relative: bool = False):
        self._heading = (self._heading + yaw_deg) % 360 if relative else yaw_deg % 360
        return {"status": "ok", "yaw_deg": self._heading}

    def _handle_set_speed(self, speed_ms: float):
        self._speed = speed_ms
        return {"status": "ok", "speed_ms": speed_ms}

    def _handle_wait_altitude(self, target_alt: float, tolerance: float = 0.5):
        return {"status": "altitude_reached", "altitude": self._altitude}

    def _handle_wait_arrival(self, tolerance_m: float = 1.0):
        return {"status": "arrived"}

    def _handle_wait_time(self, seconds: float):
        return {"status": "done", "waited_seconds": seconds}
