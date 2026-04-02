"""
MAVLink hardware backend — stub.
Set DRONE_BACKEND=mavlink in environment to activate.

To wire:
    pip install pymavlink
    Implement each _handle_*() method using self._conn (mavutil.mavlink_connection).
"""

import logging

from adapters.base_adapter import BaseAdapter

logger = logging.getLogger(__name__)


class MAVLinkAdapter(BaseAdapter):
    def __init__(self, connection_string: str = "udp:127.0.0.1:14550"):
        self._connection_string = connection_string
        self._conn = None   # will be: mavutil.mavlink_connection(connection_string)

    def is_connected(self) -> bool:
        return self._conn is not None

    def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute(self, tool_name: str, args: dict) -> dict:
        logger.info(f"[MAVLINK] {tool_name}({args})")
        handler = getattr(self, f"_handle_{tool_name}", None)
        if handler is None:
            return {"error": f"MAVLinkAdapter: no handler for '{tool_name}'"}
        return handler(**args)

    # ── Stubs — wire pymavlink commands here ─────────────────────────────────

    def _handle_connect_drone(self, connection_string=None):
        # from pymavlink import mavutil
        # self._conn = mavutil.mavlink_connection(connection_string or self._connection_string)
        # self._conn.wait_heartbeat()
        return {"error": "MAVLink not yet wired — implement _handle_connect_drone"}

    def _handle_get_current_state(self):
        return {"error": "MAVLink not yet wired — implement _handle_get_current_state"}

    def _handle_get_telemetry(self):
        return {"error": "MAVLink not yet wired — implement _handle_get_telemetry"}

    def _handle_get_position_str(self):
        return {"error": "MAVLink not yet wired — implement _handle_get_position_str"}

    def _handle_get_battery(self):
        return {"error": "MAVLink not yet wired — implement _handle_get_battery"}

    def _handle_get_distance_to_str(self, target_lat, target_lon):
        return {"error": "MAVLink not yet wired — implement _handle_get_distance_to_str"}

    def _handle_set_mode(self, mode):
        return {"error": "MAVLink not yet wired — implement _handle_set_mode"}

    def _handle_arm_drone(self):
        return {"error": "MAVLink not yet wired — implement _handle_arm_drone"}

    def _handle_disarm_drone(self):
        return {"error": "MAVLink not yet wired — implement _handle_disarm_drone"}

    def _handle_takeoff(self, altitude):
        return {"error": "MAVLink not yet wired — implement _handle_takeoff"}

    def _handle_land(self):
        return {"error": "MAVLink not yet wired — implement _handle_land"}

    def _handle_return_to_launch(self):
        return {"error": "MAVLink not yet wired — implement _handle_return_to_launch"}

    def _handle_goto_position(self, lat, lon, alt):
        return {"error": "MAVLink not yet wired — implement _handle_goto_position"}

    def _handle_set_yaw(self, yaw_deg, relative=False):
        return {"error": "MAVLink not yet wired — implement _handle_set_yaw"}

    def _handle_set_speed(self, speed_ms):
        return {"error": "MAVLink not yet wired — implement _handle_set_speed"}

    def _handle_wait_altitude(self, target_alt, tolerance=0.5):
        return {"error": "MAVLink not yet wired — implement _handle_wait_altitude"}

    def _handle_wait_arrival(self, tolerance_m=1.0):
        return {"error": "MAVLink not yet wired — implement _handle_wait_arrival"}

    def _handle_wait_time(self, seconds):
        return {"error": "MAVLink not yet wired — implement _handle_wait_time"}
