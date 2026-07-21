"""
Tests for localization/vio_slam/occupancy_grid.py.

Pure NumPy — no DepthAI, no hardware.
"""

import numpy as np
import pytest

from localization.vio_slam.occupancy_grid import LiveOccupancyGrid


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def grid():
    """Small grid: 1×1×1 m extent, 10 cm cells (20×20×10 cells with z-1..0)."""
    return LiveOccupancyGrid(cell_size=0.10, half_extent=1.0, z_min=-1.0, z_max=0.0)


# ── Coordinate round-trip ─────────────────────────────────────────────────────

class TestCoordinateRoundTrip:
    def test_origin_round_trip(self, grid):
        gx, gy, gz = grid._w2g(0.0, 0.0, -0.5)
        x, y, z = grid._g2w(gx, gy, gz)
        assert abs(x - 0.0) <= grid.cell_size
        assert abs(y - 0.0) <= grid.cell_size
        assert abs(z - (-0.5)) <= grid.cell_size

    def test_centre_cell_in_bounds(self, grid):
        gx, gy, gz = grid._w2g(0.0, 0.0, -0.5)
        assert grid._in_bounds(gx, gy, gz)

    def test_out_of_bounds_returns_false(self, grid):
        # 100 m away from the grid centre is definitely outside the 1 m extent
        gx, gy, gz = grid._w2g(100.0, 0.0, -0.5)
        assert not grid._in_bounds(gx, gy, gz)


# ── insert_obstacle_points ────────────────────────────────────────────────────

class TestInsertObstaclePoints:
    def test_single_point_marks_inflated_cube(self, grid):
        before = grid.occupied_count()
        points = np.array([[0.0, 0.0, -0.5]], dtype=np.float32)
        grid.insert_obstacle_points(points, inflate_cells=2)
        # 5×5×5 = 125 cells inflated around the point (clipped to grid bounds)
        assert grid.occupied_count() > before
        assert grid.occupied_count() <= 125

    def test_empty_points_no_change(self, grid):
        before = grid.occupied_count()
        grid.insert_obstacle_points(np.empty((0, 3)), inflate_cells=2)
        assert grid.occupied_count() == before

    def test_point_outside_grid_silently_ignored(self, grid):
        before = grid.occupied_count()
        points = np.array([[100.0, 100.0, -0.5]], dtype=np.float32)
        grid.insert_obstacle_points(points, inflate_cells=1)
        assert grid.occupied_count() == before


# ── decay ─────────────────────────────────────────────────────────────────────

class TestDecay:
    def test_decay_reduces_count_to_zero(self, grid):
        points = np.array([[0.0, 0.0, -0.5]], dtype=np.float32)
        grid.insert_obstacle_points(points, inflate_cells=1)
        for _ in range(10):
            grid.decay(amount=1)
        # After enough decays, every cell should fall below the threshold
        assert grid.occupied_count() == 0

    def test_decay_never_goes_negative(self, grid):
        # Empty grid; decay should be a no-op
        grid.decay(amount=5)
        assert grid.occupied_count() == 0
        assert int(grid.grid.min()) == 0


# ── nearest_obstacle_along ────────────────────────────────────────────────────

class TestNearestObstacleAlong:
    def test_hit_along_x_axis(self, grid):
        # Insert obstacle at x=+0.5 m (5 cells forward at 10 cm spacing)
        points = np.array([[0.5, 0.0, -0.5]], dtype=np.float32)
        grid.insert_obstacle_points(points, inflate_cells=0)
        dist = grid.nearest_obstacle_along(
            origin_xyz=(0.0, 0.0, -0.5),
            forward_xyz=(1.0, 0.0, 0.0),
            max_dist_m=2.0,
        )
        assert dist is not None
        # Allow one cell of rounding tolerance
        assert abs(dist - 0.5) <= grid.cell_size

    def test_no_obstacle_returns_none(self, grid):
        # Empty grid — no hits
        dist = grid.nearest_obstacle_along(
            origin_xyz=(0.0, 0.0, -0.5),
            forward_xyz=(1.0, 0.0, 0.0),
            max_dist_m=0.5,
        )
        assert dist is None

    def test_ray_exits_grid_returns_none(self, grid):
        # Ray starts inside, points outward — no obstacle in path
        dist = grid.nearest_obstacle_along(
            origin_xyz=(0.0, 0.0, -0.5),
            forward_xyz=(1.0, 0.0, 0.0),
            max_dist_m=100.0,
        )
        assert dist is None

    def test_zero_forward_vector_returns_none(self, grid):
        dist = grid.nearest_obstacle_along(
            origin_xyz=(0.0, 0.0, -0.5),
            forward_xyz=(0.0, 0.0, 0.0),
            max_dist_m=1.0,
        )
        assert dist is None

    def test_obstacle_beyond_max_dist_not_seen(self, grid):
        # Obstacle at 0.5 m, but cap the ray at 0.2 m
        points = np.array([[0.5, 0.0, -0.5]], dtype=np.float32)
        grid.insert_obstacle_points(points, inflate_cells=0)
        dist = grid.nearest_obstacle_along(
            origin_xyz=(0.0, 0.0, -0.5),
            forward_xyz=(1.0, 0.0, 0.0),
            max_dist_m=0.2,
        )
        assert dist is None
