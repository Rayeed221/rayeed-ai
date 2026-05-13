"""
Tests for safety_policy.SafetyPolicy — specifically the SLAM proximity gate
added in Phase 4.  Pure logic, no hardware.
"""

import time
from unittest.mock import MagicMock

import numpy as np
import pytest

from config import VIOSLAM_PROXIMITY_THR_M
from localization.vio_slam.occupancy_grid import LiveOccupancyGrid
from localization.vio_slam.slam_state import VIOPose
from safety_policy import SafetyPolicy
from state_machine import StateMachine


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sm():
    return StateMachine()


@pytest.fixture
def policy(sm):
    return SafetyPolicy(sm)


def _mock_runner(pose: VIOPose, grid: LiveOccupancyGrid):
    runner = MagicMock()
    runner.get_pose.return_value = pose
    runner.get_occupancy_grid.return_value = grid
    return runner


def _identity_pose(ts: float = None) -> VIOPose:
    if ts is None:
        ts = time.monotonic()
    return VIOPose(
        x=0.0, y=0.0, z=-0.5,
        qw=1.0, qx=0.0, qy=0.0, qz=0.0,
        heading_deg=0.0,
        source="vio",
        timestamp=ts,
    )


# ── check_slam_proximity ──────────────────────────────────────────────────────

class TestCheckSlamProximity:

    def test_returns_ok_when_runner_is_none(self, policy):
        ok, msg = policy.check_slam_proximity("goto_position")
        assert ok is True
        assert msg == ""

    def test_returns_ok_for_non_gated_tool(self, policy):
        # set up an obstacle-laden runner to prove the tool name is what gates
        grid = LiveOccupancyGrid(cell_size=0.10, half_extent=1.0, z_min=-1.0, z_max=0.0)
        # obstacle directly in front (camera Z forward → quat-identity forward is +Z)
        grid.insert_obstacle_points(np.array([[0.0, 0.0, 0.3]]), inflate_cells=0)
        policy.set_vioslam_runner(_mock_runner(_identity_pose(), grid))

        ok, _ = policy.check_slam_proximity("get_telemetry")
        assert ok is True

    def test_returns_ok_when_pose_stale(self, policy):
        from config import VIOSLAM_STALE_SEC
        old_pose = _identity_pose(ts=time.monotonic() - (VIOSLAM_STALE_SEC + 1.0))
        grid = LiveOccupancyGrid(cell_size=0.10, half_extent=1.0, z_min=-1.0, z_max=0.0)
        # put an obstacle in front; stale pose should make us SKIP the check
        grid.insert_obstacle_points(np.array([[0.0, 0.0, 0.3]]), inflate_cells=0)
        policy.set_vioslam_runner(_mock_runner(old_pose, grid))

        ok, _ = policy.check_slam_proximity("goto_position")
        assert ok is True

    def test_returns_ok_when_no_obstacle_ahead(self, policy):
        grid = LiveOccupancyGrid(cell_size=0.10, half_extent=1.0, z_min=-1.0, z_max=0.0)
        # empty grid → ray finds nothing
        policy.set_vioslam_runner(_mock_runner(_identity_pose(), grid))

        ok, _ = policy.check_slam_proximity("goto_position")
        assert ok is True

    def test_blocks_when_obstacle_within_threshold(self, policy):
        grid = LiveOccupancyGrid(cell_size=0.10, half_extent=4.0, z_min=-1.0, z_max=4.0)
        # camera Z is the forward axis for an identity quaternion (see _quat_forward).
        # Put an obstacle 0.5 m forward (z=+0.5), well inside the 1.5 m default threshold.
        grid.insert_obstacle_points(np.array([[0.0, 0.0, 0.5]]), inflate_cells=1)
        # Pose origin is at the world origin
        pose = VIOPose(x=0.0, y=0.0, z=0.0, qw=1.0, qx=0.0, qy=0.0, qz=0.0,
                       heading_deg=0.0, source="vio", timestamp=time.monotonic())
        policy.set_vioslam_runner(_mock_runner(pose, grid))

        ok, msg = policy.check_slam_proximity("goto_position")
        assert ok is False
        assert "SLAM obstacle" in msg
        # message format: "SLAM obstacle at X.XXm < THR_M"
        assert f"{VIOSLAM_PROXIMITY_THR_M}m" in msg


# ── pre_execute_check integration ─────────────────────────────────────────────

class TestPreExecuteCheckSLAM:

    def test_emits_slam_proximity_error(self, policy, sm):
        # Drone is enroute so goto_position is a legal command
        from state_machine import MissionState
        sm.transition(MissionState.CONNECTED)
        sm.transition(MissionState.ARMED)
        sm.transition(MissionState.TAKEOFF)
        sm.transition(MissionState.ENROUTE)

        # Make telemetry/battery checks pass
        policy.update_telemetry_timestamp()
        policy.update_battery(80.0)

        grid = LiveOccupancyGrid(cell_size=0.10, half_extent=4.0, z_min=-1.0, z_max=4.0)
        grid.insert_obstacle_points(np.array([[0.0, 0.0, 0.5]]), inflate_cells=1)
        pose = VIOPose(x=0.0, y=0.0, z=0.0, qw=1.0, qx=0.0, qy=0.0, qz=0.0,
                       heading_deg=0.0, source="vio", timestamp=time.monotonic())
        policy.set_vioslam_runner(_mock_runner(pose, grid))

        err = policy.pre_execute_check(
            "goto_position",
            {"lat": 0.0, "lon": 0.0, "alt_m": 5.0},
        )
        assert err is not None
        assert err.code == "SLAM_PROXIMITY"
        assert err.retryable is True
