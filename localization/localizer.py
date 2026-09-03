"""
High-level localization coordinator.

Converts camera-frame coordinates from OAK-D vision tools into:

  1. Local FRD frame (what the AI sees) — added as ``local_frame`` key
     to detection / sector dicts returned by VisionTool.

  2. Global GPS coordinates (backend only) — stored in a fixed-size deque
     as GlobalObservation instances.  Never included in ToolResponse data.

Design principle
----------------
enrich_* methods are the only public entry points.  They return a copy of
the input dict with a ``local_frame`` key appended (or the original dict
unchanged if the pose is stale / missing).  The global computation is a
silent side-effect — no error is raised if GPS is unavailable.
"""

import time
from collections import deque
from dataclasses import dataclass, field

from localization.frame_transforms import (
    camera_to_frd,
    frd_to_ned,
    ned_to_global,
    local_frame_summary,
    sector_to_frd,
)
from localization.pose_cache import PoseCache


@dataclass
class GlobalObservation:
    """
    A single detected object or obstacle expressed in global GPS coordinates.

    Stored internally in Localizer — never serialised to ToolResponse.
    """
    label_name: str
    lat:        float
    lon:        float
    alt_m:      float
    confidence: float
    timestamp:  float = field(default_factory=time.monotonic)


class Localizer:
    """
    Enriches vision tool results with local and global coordinate frames.

    Inject into VisionTool at startup.  Each enrich_* call:
      - Reads the latest DronePose from PoseCache.
      - Computes camera → FRD → NED → global transforms.
      - Appends 'local_frame' to the returned dict (AI-visible).
      - Stores a GlobalObservation in the internal deque (backend-only).

    If PoseCache.is_valid() is False (no GPS / stale data), local_frame is
    still added using whatever heading is available (or heading=0 as fallback),
    and no global observation is stored.

    Args:
        pose_cache:        shared PoseCache instance
        camera_pitch_deg:  camera tilt from drone forward-level (nose-down +)
        camera_yaw_deg:    camera rotation from drone forward axis (CW +)
        hfov_deg:          horizontal FOV of the camera in degrees
        global_store_size: max number of GlobalObservations to retain
    """

    def __init__(
        self,
        pose_cache: PoseCache,
        camera_pitch_deg: float = 0.0,
        camera_yaw_deg: float = 0.0,
        hfov_deg: float = 73.0,
        global_store_size: int = 200,
    ) -> None:
        self._pose_cache  = pose_cache
        self._pitch       = camera_pitch_deg
        self._yaw         = camera_yaw_deg
        self._hfov        = hfov_deg
        self._global_store: deque[GlobalObservation] = deque(maxlen=global_store_size)

    # ── Public enrich methods ─────────────────────────────────────────────────

    def enrich_detection(self, det: dict) -> dict:
        """
        Add ``local_frame`` to a detection dict from vision_detect_objects.

        Input keys used:  x_mm, y_mm, z_mm, label_name (optional), confidence
        Output:           shallow copy of det with 'local_frame' added

        If pose is valid, also stores a GlobalObservation (backend-only).
        """
        x_mm = det.get("x_mm", 0)
        y_mm = det.get("y_mm", 0)
        z_mm = det.get("z_mm", 0)

        pose = self._pose_cache.get()

        f_m, r_m, d_m = camera_to_frd(
            x_mm, y_mm, z_mm,
            pitch_deg=self._pitch,
            yaw_deg=self._yaw,
        )

        local = local_frame_summary(f_m, r_m, d_m)

        # Global computation (backend only — not added to returned dict)
        if pose is not None:
            self._store_global(
                f_m, r_m, d_m, pose,
                label_name=det.get("label_name", "unknown"),
                confidence=float(det.get("confidence", 0.0)),
            )

        return {**det, "local_frame": local}

    def enrich_sector(self, sector_name: str, z_m: float) -> dict:
        """
        Build an enriched sector entry for vision_obstacle_check.

        Returns a dict with ``distance_m`` and ``local_frame``.
        Never raises — falls back gracefully if pose is stale.
        """
        pose = self._pose_cache.get()

        f_m, r_m, d_m = sector_to_frd(sector_name, z_m, hfov_deg=self._hfov)

        # Apply camera mounting rotation if configured
        if self._pitch != 0.0 or self._yaw != 0.0:
            # sector_to_frd already returns approximate FRD; apply only yaw
            # correction (pitch is irrelevant for horizontal sectors)
            import math
            psi = math.radians(self._yaw)
            cos_p, sin_p = math.cos(psi), math.sin(psi)
            f_m, r_m = (
                f_m * cos_p - r_m * sin_p,
                f_m * sin_p + r_m * cos_p,
            )

        local = local_frame_summary(f_m, r_m, d_m)

        if pose is not None:
            self._store_global(
                f_m, r_m, d_m, pose,
                label_name=f"obstacle_{sector_name}",
                confidence=1.0,
            )

        return {
            "distance_m": round(z_m, 2),
            "local_frame": local,
        }

    def enrich_landing_zone(self, landing_zone: dict) -> dict:
        """
        Add ``local_frame`` to the landing zone dict from vision_depth_snapshot.

        The landing zone is directly below the camera (forward=mean_m along
        optical axis, right=0, down=0 when camera faces forward-down).
        For a level-mounted forward-facing camera the centre cell depth is
        the forward distance to the ground feature.
        """
        mean_m = landing_zone.get("mean_m") or 0.0

        # Centre cell: directly ahead along camera axis, no lateral offset
        f_m, r_m, d_m = camera_to_frd(
            0, 0, mean_m * 1000,
            pitch_deg=self._pitch,
            yaw_deg=self._yaw,
        )
        local = local_frame_summary(f_m, r_m, d_m)

        pose = self._pose_cache.get()
        if pose is not None:
            self._store_global(
                f_m, r_m, d_m, pose,
                label_name="landing_zone",
                confidence=1.0,
            )

        return {**landing_zone, "local_frame": local}

    # ── Backend-only access ───────────────────────────────────────────────────

    def global_observations(self) -> list[GlobalObservation]:
        """Return a snapshot of recent global observations (backend use only)."""
        return list(self._global_store)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _store_global(
        self,
        f_m: float,
        r_m: float,
        d_m: float,
        pose,
        label_name: str,
        confidence: float,
    ) -> None:
        """Compute global GPS position and append to the internal deque."""
        try:
            n_m, e_m, down_m = frd_to_ned(f_m, r_m, d_m, pose.heading_deg)
            lat, lon, alt_m = ned_to_global(
                n_m, e_m, down_m,
                pose.lat, pose.lon, pose.alt_m,
            )
            self._global_store.append(GlobalObservation(
                label_name=label_name,
                lat=round(lat, 7),
                lon=round(lon, 7),
                alt_m=round(alt_m, 2),
                confidence=confidence,
            ))
        except Exception:
            # Global computation is best-effort; never crash the vision tool
            pass
