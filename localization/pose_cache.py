"""
Thread-safe drone pose cache.

Three independent writers feed this cache:

  - TelemetryReader   — heading, altitude         (every 2 s)
  - PositionMonitor   — lat, lon (+ alt fallback) (every 5 s)
  - VIOSLAMRunner     — heading from VIO yaw + full VIOPose snapshot (every frame)

Reads merge them into a single DronePose:

  - lat / lon / alt come from GPS+telemetry (VIO has no global frame).
  - heading_deg comes from VIO if fresh (<= VIOSLAM_STALE_SEC old), otherwise
    from telemetry.  This makes VIO the priority source for orientation while
    leaving global position untouched.

`get()` still returns None unless lat, lon, alt, and *some* heading source are
all available — preserving its existing contract.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from config import VIOSLAM_STALE_SEC

if TYPE_CHECKING:
    from localization.vio_slam.slam_state import VIOPose


@dataclass
class DronePose:
    """Snapshot of drone state used for coordinate frame transforms."""
    lat:         float   # decimal degrees
    lon:         float   # decimal degrees
    alt_m:       float   # AGL metres
    heading_deg: float   # 0–360, 0 = North
    timestamp:   float = field(default_factory=time.monotonic)


class PoseCache:
    """
    Thread-safe cache that merges telemetry, GPS, and VIO updates.

    See module docstring for the merge policy.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

        # Global position — only GPS / position monitor writes these
        self._lat:               Optional[float] = None
        self._lon:               Optional[float] = None
        self._alt_m:             Optional[float] = None

        # Heading has two independent sources resolved at read time
        self._heading_deg_tel:   Optional[float] = None
        self._heading_deg_vio:   Optional[float] = None
        self._vio_heading_ts:    float           = 0.0

        # Full VIO pose for callers that want body-frame coordinates
        self._vio_pose:          Optional["VIOPose"] = None

        # Most recent write of any kind — used by is_valid()
        self._last_update:       float           = 0.0

    # ── Writers ───────────────────────────────────────────────────────────────

    def update_telemetry(self, alt_m: float, heading_deg: float) -> None:
        """Update altitude and heading from a get_telemetry() response."""
        with self._lock:
            self._alt_m             = float(alt_m)
            self._heading_deg_tel   = float(heading_deg)
            self._last_update       = time.monotonic()

    def update_position(self, lat: float, lon: float, alt_m: float) -> None:
        """Update GPS coordinates from a parsed get_position_str() response."""
        with self._lock:
            self._lat = float(lat)
            self._lon = float(lon)
            if self._alt_m is None:
                self._alt_m = float(alt_m)
            self._last_update = time.monotonic()

    def update_from_vio(self, vio_pose: "VIOPose") -> None:
        """Update from a VIOSLAMRunner tick — heading + raw body-frame pose."""
        with self._lock:
            self._heading_deg_vio = float(vio_pose.heading_deg)
            self._vio_pose        = vio_pose
            self._vio_heading_ts  = time.monotonic()
            self._last_update     = self._vio_heading_ts

    # ── Internal heading resolver ─────────────────────────────────────────────

    def _resolve_heading_locked(self) -> Optional[float]:
        """Return VIO heading if fresh, else telemetry, else None.  Lock held."""
        if self._heading_deg_vio is not None:
            age = time.monotonic() - self._vio_heading_ts
            if age <= VIOSLAM_STALE_SEC:
                return self._heading_deg_vio
        return self._heading_deg_tel

    # ── Readers ───────────────────────────────────────────────────────────────

    def get(self) -> Optional[DronePose]:
        """
        Return the latest DronePose, or None if any required field is missing.

        All four fields (lat, lon, alt_m, heading_deg) must have been received
        at least once.  `heading_deg` comes from VIO when fresh, otherwise from
        telemetry.
        """
        with self._lock:
            if None in (self._lat, self._lon, self._alt_m):
                return None
            heading = self._resolve_heading_locked()
            if heading is None:
                return None
            return DronePose(
                lat=self._lat,
                lon=self._lon,
                alt_m=self._alt_m,
                heading_deg=heading,
                timestamp=self._last_update,
            )

    def get_vio_pose(self) -> Optional["VIOPose"]:
        """Return the most recent VIOPose (frozen dataclass, safe to share)."""
        with self._lock:
            return self._vio_pose

    def is_valid(self, max_age_s: float = 10.0) -> bool:
        """True if a complete pose is available and was updated recently."""
        with self._lock:
            if None in (self._lat, self._lon, self._alt_m):
                return False
            if self._resolve_heading_locked() is None:
                return False
            return (time.monotonic() - self._last_update) <= max_age_s
