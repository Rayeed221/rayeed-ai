"""
Thread-safe state dataclasses published by VIOSLAMRunner.

Both are frozen so they can be passed across threads without defensive copying.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VIOPose:
    """6-DOF pose snapshot in the VIO start frame (metres, quaternion)."""
    x: float
    y: float
    z: float
    qw: float
    qx: float
    qy: float
    qz: float
    heading_deg: float   # yaw extracted from quaternion, 0-360
    source: str          # "vio" (raw odometry) or "slam" (loop-closure corrected)
    timestamp: float     # time.monotonic()


@dataclass(frozen=True)
class SLAMSnapshot:
    """Aggregate state of the occupancy grid at one instant."""
    occupied_cells: int
    grid_origin_xy: tuple   # (x, y) grid centre in VIO frame
    timestamp: float        # time.monotonic()
