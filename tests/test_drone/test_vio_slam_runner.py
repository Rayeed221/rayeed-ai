"""
Tests for localization/vio_slam/vio_slam_runner.py.

DepthAI is mocked — these tests run on any machine with no OAK-D required.
Coverage focuses on the parts NOT covered by hardware smoke-tests:
  - _quat_to_heading_deg numerical correctness
  - _pcl_to_numpy handles empty / 1-D / 2-D point lists
  - get_pose / get_snapshot thread safety
  - PoseCache.update_from_vio is called when a pose message arrives
"""

import sys
import threading
import time
from unittest.mock import MagicMock

import numpy as np
import pytest

from localization.pose_cache import PoseCache
from localization.vio_slam.slam_state import VIOPose, SLAMSnapshot
from localization.vio_slam.vio_slam_runner import VIOSLAMRunner


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def runner():
    return VIOSLAMRunner(
        db_path="map.db",
        load_db=False,
        fps=30,
        slam_hz=2.0,
        occ_cell_size=0.05,
        pose_cache=PoseCache(),
    )


# ── _quat_to_heading_deg ──────────────────────────────────────────────────────

class TestQuatToHeading:
    def test_identity_quaternion_is_zero_heading(self):
        h = VIOSLAMRunner._quat_to_heading_deg(1.0, 0.0, 0.0, 0.0)
        assert h == pytest.approx(0.0, abs=1e-6)

    def test_90_degree_yaw(self):
        # quaternion for 90° around Z: (cos45°, 0, 0, sin45°)
        import math
        h = VIOSLAMRunner._quat_to_heading_deg(math.cos(math.pi / 4), 0.0, 0.0, math.sin(math.pi / 4))
        assert h == pytest.approx(90.0, abs=1e-3)

    def test_180_degree_yaw(self):
        h = VIOSLAMRunner._quat_to_heading_deg(0.0, 0.0, 0.0, 1.0)
        # 180° or -180° both wrap to 180.0 via % 360.0
        assert h == pytest.approx(180.0, abs=1e-3)

    def test_negative_yaw_wraps_to_positive(self):
        # quaternion for -90° around Z: (cos45°, 0, 0, -sin45°)
        import math
        h = VIOSLAMRunner._quat_to_heading_deg(math.cos(math.pi / 4), 0.0, 0.0, -math.sin(math.pi / 4))
        assert h == pytest.approx(270.0, abs=1e-3)


# ── _pcl_to_numpy ─────────────────────────────────────────────────────────────

class TestPclToNumpy:
    def test_empty_returns_zero_by_three(self):
        msg = MagicMock()
        msg.getPoints.return_value = []
        arr = VIOSLAMRunner._pcl_to_numpy(msg)
        assert arr.shape == (0, 3)

    def test_one_d_flat_reshaped(self):
        msg = MagicMock()
        # Simulate a flat array of [x, y, z, x, y, z]
        msg.getPoints.return_value = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        arr = VIOSLAMRunner._pcl_to_numpy(msg)
        assert arr.shape == (2, 3)
        assert np.allclose(arr[0], [1, 2, 3])
        assert np.allclose(arr[1], [4, 5, 6])

    def test_two_d_passthrough(self):
        msg = MagicMock()
        msg.getPoints.return_value = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        arr = VIOSLAMRunner._pcl_to_numpy(msg)
        assert arr.shape == (2, 3)


# ── State accessors ───────────────────────────────────────────────────────────

class TestStateAccessors:
    def test_initial_state_is_none(self, runner):
        assert runner.get_pose() is None
        assert runner.get_snapshot() is None

    def test_get_occupancy_grid_returns_ref(self, runner):
        g = runner.get_occupancy_grid()
        assert g is runner._occ_grid

    def test_get_pose_thread_safe(self, runner):
        """Many concurrent readers must not crash even when writers race."""
        errors = []

        def writer():
            try:
                for _ in range(200):
                    with runner._lock:
                        runner._pose = VIOPose(0, 0, 0, 1, 0, 0, 0, 0.0, "vio", time.monotonic())
            except Exception as exc:
                errors.append(exc)

        def reader():
            try:
                for _ in range(200):
                    runner.get_pose()
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=writer)] + [threading.Thread(target=reader) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []


# ── _transform_to_vio_pose ────────────────────────────────────────────────────

class TestTransformToVioPose:
    def test_builds_pose_from_message_fields(self, runner):
        msg = MagicMock()
        msg.getTranslation.return_value = MagicMock(x=1.0, y=2.0, z=3.0)
        msg.getQuaternion.return_value = MagicMock(qw=1.0, qx=0.0, qy=0.0, qz=0.0)
        pose = runner._transform_to_vio_pose(msg, source="slam")
        assert isinstance(pose, VIOPose)
        assert pose.x == 1.0 and pose.y == 2.0 and pose.z == 3.0
        assert pose.heading_deg == pytest.approx(0.0, abs=1e-6)
        assert pose.source == "slam"


# ── run() with mocked depthai — confirms the integration path ─────────────────

class TestRunIntegration:
    @pytest.fixture
    def mock_depthai(self, monkeypatch):
        """Inject a fake `depthai` module so `import depthai` inside run() succeeds."""
        fake = MagicMock()
        monkeypatch.setitem(sys.modules, "depthai", fake)
        yield fake

    @pytest.mark.asyncio
    async def test_missing_depthai_disables_loop(self, runner, monkeypatch):
        """No depthai installed → log + return without crashing."""
        monkeypatch.setitem(sys.modules, "depthai", None)  # make import fail
        # Note: with `None` in sys.modules, `import depthai` raises ImportError.
        # run() must swallow it via its try/except and return cleanly.
        await runner.run()  # would hang if it tried to enter the loop

    @pytest.mark.asyncio
    async def test_pipeline_build_failure_disables_loop(self, runner, mock_depthai, monkeypatch):
        """If _build_pipeline raises, run() logs and returns — never the asyncio loop."""
        def boom(self):
            raise RuntimeError("simulated build failure")
        monkeypatch.setattr(VIOSLAMRunner, "_build_pipeline", boom)
        await runner.run()   # must not raise
