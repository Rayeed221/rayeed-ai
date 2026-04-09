"""
Thread-safe drone pose cache.

Updated by TelemetryReader (heading, altitude every 2 s) and
PositionMonitor (lat/lon every 5 s).  Provides a consistent snapshot
for coordinate frame transforms.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DronePose:
    """Snapshot of drone state used for coordinate frame transforms."""
    lat:         float   # decimal degrees
    lon:         float   # decimal degrees
    alt_m:       float   # AGL metres
    heading_deg: float   # 0–360, magnetic heading (0 = North)
    timestamp:   float = field(default_factory=time.monotonic)


class PoseCache:
    """
    Thread-safe cache that merges telemetry (heading, altitude) and
    GPS position (lat, lon) into a single DronePose.

    Telemetry and position are polled on different intervals (2 s vs 5 s),
    so the cache keeps the last known value of each independently and
    combines them on demand.

    Usage
    -----
    pose_cache = PoseCache()

    # Called by TelemetryReader after each successful get_telemetry():
    pose_cache.update_telemetry(alt_m=5.0, heading_deg=90.0)

    # Called by PositionMonitor after each successful get_position_str():
    pose_cache.update_position(lat=23.81, lon=90.41, alt_m=5.0)

    # Called by Localizer before each transform:
    pose = pose_cache.get()
    if pose_cache.is_valid():
        ...
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # Each field updated independently; None until first update
        self._lat:         Optional[float] = None
        self._lon:         Optional[float] = None
        self._alt_m:       Optional[float] = None
        self._heading_deg: Optional[float] = None
        self._last_update: float = 0.0

    # ── Update methods (called from async tasks via asyncio.to_thread or directly) ─

    def update_telemetry(self, alt_m: float, heading_deg: float) -> None:
        """Update altitude and heading from a get_telemetry() response."""
        with self._lock:
            self._alt_m       = float(alt_m)
            self._heading_deg = float(heading_deg)
            self._last_update = time.monotonic()

    def update_position(self, lat: float, lon: float, alt_m: float) -> None:
        """Update GPS coordinates from a parsed get_position_str() response."""
        with self._lock:
            self._lat   = float(lat)
            self._lon   = float(lon)
            # Position monitor also provides alt — use it to fill the field
            # if telemetry hasn't set it yet.
            if self._alt_m is None:
                self._alt_m = float(alt_m)
            self._last_update = time.monotonic()

    # ── Query methods ────────────────────────────────────────────────────────────

    def get(self) -> Optional[DronePose]:
        """
        Return the latest DronePose, or None if any required field is missing.

        All four fields (lat, lon, alt_m, heading_deg) must have been received
        at least once for a valid pose to be returned.
        """
        with self._lock:
            if None in (self._lat, self._lon, self._alt_m, self._heading_deg):
                return None
            return DronePose(
                lat=self._lat,
                lon=self._lon,
                alt_m=self._alt_m,
                heading_deg=self._heading_deg,
                timestamp=self._last_update,
            )

    def is_valid(self, max_age_s: float = 10.0) -> bool:
        """
        Return True if a complete pose is available and was updated recently.

        Args:
            max_age_s: maximum acceptable age of the last update in seconds
        """
        with self._lock:
            if None in (self._lat, self._lon, self._alt_m, self._heading_deg):
                return False
            return (time.monotonic() - self._last_update) <= max_age_s
