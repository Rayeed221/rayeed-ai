"""
Rolling 3D occupancy grid updated from SLAM obstacle point clouds.

Lifted from tests/test_depthai/testing/live_slam_avoidance_FINAL.py (the
exploration script).  Pure NumPy — no DepthAI dependency, fully testable
without hardware.

Conventions:
  - Coordinates are in the VIO start frame (metres).
  - Grid centre is `(origin_x, origin_y)` in that frame.  z spans z_min..z_max.
  - Each cell stores a hit count (int16); cell counts as occupied when
    count >= obstacle_thresh.  Decaying counts lets stale obstacles fade.
"""

from typing import Optional

import numpy as np


class LiveOccupancyGrid:
    def __init__(
        self,
        cell_size: float = 0.05,   # matches config.VIOSLAM_OCC_CELL_SIZE / SLAM Grid/CellSize
        half_extent: float = 8.0,
        z_min: float = -1.0,
        z_max: float = 4.0,
    ):
        self.cell_size = cell_size
        self.half_extent = half_extent
        self.z_min = z_min
        self.z_max = z_max

        side = int(2 * half_extent / cell_size)
        z_cells = int((z_max - z_min) / cell_size)
        self.nx, self.ny, self.nz = side, side, z_cells

        self.grid = np.zeros((self.nx, self.ny, self.nz), dtype=np.int16)
        self.obstacle_thresh = 1

        self.origin_x = 0.0
        self.origin_y = 0.0

    # ── Coordinate helpers ────────────────────────────────────────────────────

    def _w2g(self, x: float, y: float, z: float) -> tuple:
        gx = int((x - self.origin_x + self.half_extent) / self.cell_size)
        gy = int((y - self.origin_y + self.half_extent) / self.cell_size)
        gz = int((z - self.z_min) / self.cell_size)
        return gx, gy, gz

    def _g2w(self, gx: int, gy: int, gz: int) -> tuple:
        x = gx * self.cell_size + self.origin_x - self.half_extent
        y = gy * self.cell_size + self.origin_y - self.half_extent
        z = gz * self.cell_size + self.z_min
        return x, y, z

    def _in_bounds(self, gx: int, gy: int, gz: int) -> bool:
        return 0 <= gx < self.nx and 0 <= gy < self.ny and 0 <= gz < self.nz

    def is_free(self, gx: int, gy: int, gz: int) -> bool:
        if not self._in_bounds(gx, gy, gz):
            return False
        return self.grid[gx, gy, gz] < self.obstacle_thresh

    # ── Updates from point cloud data ─────────────────────────────────────────

    def insert_obstacle_points(self, points, inflate_cells: int = 2) -> None:
        """Insert obstacle points (Nx3 ndarray) with cell inflation."""
        for pt in points:
            cx, cy, cz = self._w2g(pt[0], pt[1], pt[2])
            for dx in range(-inflate_cells, inflate_cells + 1):
                for dy in range(-inflate_cells, inflate_cells + 1):
                    for dz in range(-inflate_cells, inflate_cells + 1):
                        nx, ny, nz = cx + dx, cy + dy, cz + dz
                        if self._in_bounds(nx, ny, nz):
                            self.grid[nx, ny, nz] += 1

    def mark_free_along_ray(self, origin, point, step: Optional[float] = None) -> None:
        """Decrement obstacle counts along a ray (free-space carving)."""
        if step is None:
            step = self.cell_size
        direction = np.array(point) - np.array(origin)
        dist = float(np.linalg.norm(direction))
        if dist < 1e-6:
            return
        direction = direction / dist
        t = 0.0
        while t < dist - step:
            p = np.array(origin) + direction * t
            gx, gy, gz = self._w2g(p[0], p[1], p[2])
            if self._in_bounds(gx, gy, gz):
                self.grid[gx, gy, gz] = max(0, int(self.grid[gx, gy, gz]) - 1)
            t += step

    def decay(self, amount: int = 1) -> None:
        """Reduce obstacle counts so stale obstacles fade."""
        mask = self.grid > 0
        self.grid[mask] = np.maximum(0, self.grid[mask] - amount)

    def occupied_count(self) -> int:
        return int(np.sum(self.grid >= self.obstacle_thresh))

    # ── Queries used by the safety policy ─────────────────────────────────────

    def nearest_obstacle_along(
        self,
        origin_xyz,
        forward_xyz,
        max_dist_m: float = 8.0,
    ) -> Optional[float]:
        """
        Ray-cast forward from origin and return distance (metres) to the first
        occupied cell.  Returns None if the ray exits the grid or reaches
        max_dist_m without hitting an obstacle.

        origin_xyz / forward_xyz may be tuples, lists, or ndarrays.
        """
        origin = np.asarray(origin_xyz, dtype=float)
        forward = np.asarray(forward_xyz, dtype=float)
        norm = float(np.linalg.norm(forward))
        if norm < 1e-9:
            return None
        forward = forward / norm

        step = self.cell_size
        t = 0.0
        while t <= max_dist_m:
            p = origin + forward * t
            gx, gy, gz = self._w2g(p[0], p[1], p[2])
            if not self._in_bounds(gx, gy, gz):
                return None
            if self.grid[gx, gy, gz] >= self.obstacle_thresh:
                return t
            t += step
        return None
