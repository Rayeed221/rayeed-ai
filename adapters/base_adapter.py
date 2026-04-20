from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """
    Abstract base for all drone execution backends.
    All methods are synchronous — dispatcher wraps them with asyncio.to_thread.
    """

    @abstractmethod
    def execute(self, tool_name: str, args: dict) -> dict:
        """Execute a named tool and return a raw result dict."""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @abstractmethod
    def snapshot(self) -> dict:
        """
        Return a unified snapshot of live drone state.
        Must always return a dict; missing fields may be absent on new connections.

        Expected keys (present when data is available):
            connected, armed, mode, system_status, landed_state,
            altitude, airspeed, groundspeed, heading,
            lat, lon, home_lat, home_lon, home_set,
            voltage, current, battery_pct,
            ekf_ok, wp_dist, timestamp
        """
        ...
