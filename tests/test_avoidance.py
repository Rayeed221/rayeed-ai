"""
Tests for the GRU-based obstacle avoidance system.

All hardware dependencies (ONNX Runtime session, DepthAI device) are mocked
via unittest.mock so no physical hardware is required.

Run:
    pytest tests/test_avoidance.py -v
"""

import math
import os
import tempfile

import numpy as np
import pytest
import torch
from unittest.mock import MagicMock, patch


# ── DepthEncoder ──────────────────────────────────────────────────────────────

def test_depth_encoder_output_shape():
    from avoidance.depth_encoder import DepthEncoder
    model = DepthEncoder()
    model.eval()
    x = torch.zeros(1, 1, 128, 128, dtype=torch.float32)
    with torch.no_grad():
        out = model(x)
    assert out.shape == (1, 64), f"Expected (1, 64), got {out.shape}"


def test_depth_encoder_batch_shape():
    from avoidance.depth_encoder import DepthEncoder
    model = DepthEncoder()
    model.eval()
    x = torch.zeros(4, 1, 128, 128, dtype=torch.float32)
    with torch.no_grad():
        out = model(x)
    assert out.shape == (4, 64), f"Expected (4, 64), got {out.shape}"


# ── ObstacleAvoidanceGRU ──────────────────────────────────────────────────────

def test_gru_output_shape():
    from avoidance.gru_model import ObstacleAvoidanceGRU
    model = ObstacleAvoidanceGRU()
    model.eval()
    x = torch.zeros(1, 1, 80)
    h = torch.zeros(1, 1, 128)
    with torch.no_grad():
        correction, h_new = model(x, h)
    assert correction.shape == (1, 3),   f"Expected (1,3), got {correction.shape}"
    assert h_new.shape    == (1, 1, 128), f"Expected (1,1,128), got {h_new.shape}"


def test_gru_correction_bounded():
    """Tanh × MAX_CORRECTION must keep correction within bounds."""
    from avoidance.gru_model import ObstacleAvoidanceGRU
    model = ObstacleAvoidanceGRU()
    model.eval()
    max_val = ObstacleAvoidanceGRU.MAX_CORRECTION
    for _ in range(10):
        x = torch.randn(1, 1, 80)
        h = torch.randn(1, 1, 128)
        with torch.no_grad():
            correction, _ = model(x, h)
        assert correction.abs().max().item() <= max_val + 1e-5, \
            f"Correction exceeded bound: {correction.abs().max().item()}"


def test_gru_hidden_state_propagation():
    """Hidden state must change on each forward pass."""
    from avoidance.gru_model import ObstacleAvoidanceGRU
    model = ObstacleAvoidanceGRU()
    model.eval()
    x  = torch.randn(1, 1, 80)
    h0 = torch.zeros(1, 1, 128)
    with torch.no_grad():
        _, h1 = model(x, h0)
        _, h2 = model(x, h1)
    assert not torch.allclose(h0, h1), "h1 must differ from h0"
    assert not torch.allclose(h1, h2), "h2 must differ from h1"


# ── preprocess_depth_for_oakd ─────────────────────────────────────────────────

def test_preprocess_depth_output_shape():
    from avoidance.dataset import preprocess_depth_for_oakd
    depth = np.ones((480, 640), dtype=np.float32) * 5.0
    out = preprocess_depth_for_oakd(depth)
    assert out.shape == (128, 128), f"Expected (128,128), got {out.shape}"


def test_preprocess_depth_output_range():
    from avoidance.dataset import preprocess_depth_for_oakd
    rng = np.random.default_rng(42)
    depth = rng.uniform(0.1, 15.0, size=(256, 320)).astype(np.float32)
    out = preprocess_depth_for_oakd(depth)
    assert out.min() >= 0.0 - 1e-5, f"min={out.min():.6f} below 0"
    assert out.max() <= 1.0 + 1e-5, f"max={out.max():.6f} above 1"


def test_preprocess_depth_dtype():
    from avoidance.dataset import preprocess_depth_for_oakd
    depth = np.ones((128, 128), dtype=np.float64) * 3.0
    out = preprocess_depth_for_oakd(depth)
    assert out.dtype == np.float32


# ── generate_gru_sequences ────────────────────────────────────────────────────

def _make_rollout(directory, T):
    """Helper: write fake rollout .npy files with T timesteps."""
    np.save(os.path.join(directory, "depth.npy"),       np.zeros((T, 64, 64), dtype=np.float32))
    np.save(os.path.join(directory, "imu.npy"),         np.zeros((T, 6),      dtype=np.float32))
    np.save(os.path.join(directory, "vel.npy"),         np.zeros((T, 3),      dtype=np.float32))
    np.save(os.path.join(directory, "attitude.npy"),    np.zeros((T, 4),      dtype=np.float32))
    np.save(os.path.join(directory, "goal_offset.npy"), np.zeros((T, 3),      dtype=np.float32))
    np.save(os.path.join(directory, "correction.npy"),  np.zeros((T, 3),      dtype=np.float32))


def test_generate_sequences_no_boundary_crossing():
    """Windows must not span multiple rollout directories."""
    from avoidance.dataset import generate_gru_sequences

    N = 5
    T = 8  # → windows at [0:5],[1:6],[2:7],[3:8] = 4 windows per rollout

    with tempfile.TemporaryDirectory() as root:
        for name in ["rollout_0", "rollout_1"]:
            d = os.path.join(root, name)
            os.makedirs(d)
            _make_rollout(d, T)

        seqs = generate_gru_sequences(root, N=N, stride=1)

    expected = 2 * (T - N + 1)
    assert len(seqs) == expected, f"Expected {expected} sequences, got {len(seqs)}"


def test_generate_sequences_window_length():
    """Each sequence must have exactly N timesteps."""
    from avoidance.dataset import generate_gru_sequences

    N = 5
    with tempfile.TemporaryDirectory() as root:
        d = os.path.join(root, "rollout_0")
        os.makedirs(d)
        _make_rollout(d, 10)

        seqs = generate_gru_sequences(root, N=N, stride=1)

    for depths, imus, vels, atts, goals, corr in seqs:
        assert len(depths) == N
        assert len(imus)   == N


def test_generate_sequences_skips_short_rollouts():
    """Rollouts shorter than N must be skipped."""
    from avoidance.dataset import generate_gru_sequences

    N = 5
    with tempfile.TemporaryDirectory() as root:
        d = os.path.join(root, "rollout_short")
        os.makedirs(d)
        _make_rollout(d, N - 1)  # too short

        seqs = generate_gru_sequences(root, N=N, stride=1)

    assert len(seqs) == 0


# ── AvoidanceController — fixture ─────────────────────────────────────────────

@pytest.fixture
def ctrl():
    """AvoidanceController with all hardware dependencies mocked."""
    from avoidance_controller import AvoidanceController

    mock_master                    = MagicMock()
    mock_master.target_system      = 1
    mock_master.target_component   = 1
    mock_master.mav                = MagicMock()

    mock_safety = MagicMock()
    mock_gru    = MagicMock()
    mock_oak    = MagicMock()

    controller = AvoidanceController(mock_master, mock_safety, mock_gru, mock_oak)
    controller._origin_lat = 0.0
    controller._origin_lon = 0.0
    controller._origin_alt = 0.0
    return controller


# ── _gps_to_ned ───────────────────────────────────────────────────────────────

def test_gps_to_ned_north(ctrl):
    """0.001° north ≈ 111.1 m north, zero east and down."""
    ned = ctrl._gps_to_ned(0.001, 0.0, 0.0)
    assert abs(ned[0] - 111.1) < 1.0,  f"N={ned[0]:.2f}"
    assert abs(ned[1])         < 0.1,  f"E={ned[1]:.4f}"
    assert abs(ned[2])         < 0.1,  f"D={ned[2]:.4f}"


def test_gps_to_ned_east(ctrl):
    """0.001° east ≈ 111.1 m east at equator, zero north."""
    ned = ctrl._gps_to_ned(0.0, 0.001, 0.0)
    assert abs(ned[0])         < 0.1,  f"N={ned[0]:.4f}"
    assert abs(ned[1] - 111.1) < 1.0, f"E={ned[1]:.2f}"


def test_gps_to_ned_altitude(ctrl):
    """MSL 100 m above origin → NED down = -100 m."""
    ned = ctrl._gps_to_ned(0.0, 0.0, 100.0)
    assert abs(ned[2] - (-100.0)) < 0.1, f"D={ned[2]:.4f}"


# ── _body_to_ned ──────────────────────────────────────────────────────────────

def test_body_to_ned_zero_yaw(ctrl):
    """Yaw=0: body X (forward) → NED North."""
    body = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    ned  = ctrl._body_to_ned(body, 0.0)
    assert abs(ned[0] - 1.0) < 1e-5, f"N={ned[0]}"
    assert abs(ned[1])       < 1e-5, f"E={ned[1]}"


def test_body_to_ned_90_yaw(ctrl):
    """Yaw=90°: body X → NED East."""
    body = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    ned  = ctrl._body_to_ned(body, math.pi / 2)
    assert abs(ned[0])       < 1e-5, f"N={ned[0]}"
    assert abs(ned[1] - 1.0) < 1e-5, f"E={ned[1]}"


def test_body_to_ned_180_yaw(ctrl):
    """Yaw=180°: body X → NED South (negative North)."""
    body = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    ned  = ctrl._body_to_ned(body, math.pi)
    assert abs(ned[0] - (-1.0)) < 1e-4, f"N={ned[0]}"
    assert abs(ned[1])           < 1e-4, f"E={ned[1]}"


def test_body_to_ned_down_unchanged(ctrl):
    """Down component passes through unchanged regardless of yaw."""
    body = np.array([0.0, 0.0, 2.5], dtype=np.float32)
    for yaw in [0.0, math.pi / 4, math.pi / 2, math.pi]:
        ned = ctrl._body_to_ned(body, yaw)
        assert abs(ned[2] - 2.5) < 1e-5, f"D={ned[2]} at yaw={math.degrees(yaw):.0f}°"


# ── _decompose_path ───────────────────────────────────────────────────────────

def test_decompose_path_short(ctrl):
    """Path shorter than spacing → exactly 1 sub-goal = end."""
    start = np.zeros(3, dtype=np.float32)
    end   = np.array([1.5, 0.0, 0.0], dtype=np.float32)
    subs  = ctrl._decompose_path(start, end)
    assert len(subs) == 1
    assert np.allclose(subs[-1], end, atol=1e-4)


def test_decompose_path_spacing(ctrl):
    """10 m path at 2 m spacing → 5 sub-goals, each 2 m apart."""
    start = np.zeros(3, dtype=np.float32)
    end   = np.array([10.0, 0.0, 0.0], dtype=np.float32)
    subs  = ctrl._decompose_path(start, end)
    assert len(subs) == 5
    for i, sub in enumerate(subs):
        expected_n = (i + 1) * 2.0
        assert abs(sub[0] - expected_n) < 0.01, f"sub[{i}].N={sub[0]:.3f}"


def test_decompose_path_last_is_goal(ctrl):
    """Last sub-goal must be exactly the end point for arrival detection."""
    start = np.zeros(3, dtype=np.float32)
    end   = np.array([7.3, 2.1, -0.5], dtype=np.float32)
    subs  = ctrl._decompose_path(start, end)
    assert np.allclose(subs[-1], end, atol=0.01), \
        f"Last sub-goal {subs[-1]} != end {end}"


def test_decompose_path_3d(ctrl):
    """Decomposition works for 3D paths (with altitude change)."""
    start = np.zeros(3, dtype=np.float32)
    end   = np.array([6.0, 0.0, -6.0], dtype=np.float32)  # 45° diagonal
    subs  = ctrl._decompose_path(start, end)
    assert len(subs) >= 1
    assert np.allclose(subs[-1], end, atol=0.01)


# ── _euler_to_quat ────────────────────────────────────────────────────────────

def test_euler_to_quat_identity():
    """Zero Euler angles → identity quaternion [1,0,0,0]."""
    from avoidance_controller import AvoidanceController
    q = AvoidanceController._euler_to_quat(0.0, 0.0, 0.0)
    assert abs(q[0] - 1.0) < 1e-6, f"w={q[0]}"
    assert abs(q[1])        < 1e-6, f"x={q[1]}"
    assert abs(q[2])        < 1e-6, f"y={q[2]}"
    assert abs(q[3])        < 1e-6, f"z={q[3]}"


def test_euler_to_quat_unit_norm():
    """Quaternion must always have unit norm."""
    from avoidance_controller import AvoidanceController
    for roll, pitch, yaw in [(0.1, 0.2, 0.3), (1.0, -0.5, 2.0), (0, 0, math.pi)]:
        q = AvoidanceController._euler_to_quat(roll, pitch, yaw)
        norm = float(np.linalg.norm(q))
        assert abs(norm - 1.0) < 1e-5, f"norm={norm:.6f} for r={roll},p={pitch},y={yaw}"


# ── Watchdog: NaN correction detection ───────────────────────────────────────

@pytest.mark.asyncio
async def test_control_step_nan_disables_avoidance(ctrl):
    """NaN GRU output must disable avoidance and reset hidden state."""
    import asyncio

    # Set up a goal and sub-goals
    ctrl._goal_event = asyncio.Event()
    ctrl._goal_event.set()
    ctrl._goal_ned        = np.array([5.0, 0.0, 0.0], dtype=np.float32)
    ctrl._sub_goals       = [np.array([5.0, 0.0, 0.0], dtype=np.float32)]
    ctrl._current_sub_idx = 0
    ctrl._avoidance_enabled = True
    ctrl._h = np.ones((1, 1, 128), dtype=np.float32)  # dirty hidden state

    # Mock OAK-D encoder queue returning a zero feature vector
    mock_data = MagicMock()
    mock_data.getFirstLayerFp16.return_value = [0.0] * 64
    mock_queue = MagicMock()
    mock_queue.tryGet.return_value = mock_data
    ctrl._oak.getOutputQueue.return_value = mock_queue
    ctrl._last_frame_time = 1.0  # non-zero so no frame timeout

    # Mock GRU returning NaN correction
    nan_correction = np.full((1, 3), float("nan"), dtype=np.float32)
    h_out          = np.zeros((1, 1, 128), dtype=np.float32)
    ctrl._gru.run.return_value = [nan_correction, h_out]

    await ctrl._control_step()

    assert ctrl._avoidance_enabled is False, "avoidance must be disabled on NaN"
    assert np.all(ctrl._h == 0.0),           "hidden state must be reset to zeros"


@pytest.mark.asyncio
async def test_control_step_divergence_resets_hidden(ctrl):
    """Correction > _DIVERGENCE_THRESHOLD_M resets hidden state but keeps avoidance enabled."""
    import asyncio
    from avoidance_controller import _DIVERGENCE_THRESHOLD_M

    ctrl._goal_event = asyncio.Event()
    ctrl._goal_event.set()
    ctrl._goal_ned        = np.array([5.0, 0.0, 0.0], dtype=np.float32)
    ctrl._sub_goals       = [np.array([5.0, 0.0, 0.0], dtype=np.float32)]
    ctrl._current_sub_idx = 0
    ctrl._avoidance_enabled = True
    ctrl._h = np.ones((1, 1, 128), dtype=np.float32)

    # Mock OAK-D
    mock_data = MagicMock()
    mock_data.getFirstLayerFp16.return_value = [0.0] * 64
    mock_queue = MagicMock()
    mock_queue.tryGet.return_value = mock_data
    ctrl._oak.getOutputQueue.return_value = mock_queue
    ctrl._last_frame_time = 1.0

    # Divergent correction (> threshold)
    big_correction = np.array([[_DIVERGENCE_THRESHOLD_M + 1.0, 0.0, 0.0]], dtype=np.float32)
    h_out          = np.zeros((1, 1, 128), dtype=np.float32)
    ctrl._gru.run.return_value = [big_correction, h_out]

    await ctrl._control_step()

    # Avoidance must still be enabled (only hidden state reset)
    assert ctrl._avoidance_enabled is True, "avoidance should stay enabled on divergence"
    assert np.all(ctrl._h == 0.0),          "hidden state must be reset"


# ── set_goal resets hidden state ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_set_goal_resets_hidden_state(ctrl):
    """set_goal() must always zero the GRU hidden state."""
    import asyncio

    ctrl._goal_event = asyncio.Event()
    ctrl._h = np.ones((1, 1, 128), dtype=np.float32)
    ctrl._pos_ned = np.zeros(3, dtype=np.float32)

    await ctrl.set_goal(0.001, 0.001, 50.0)

    assert np.all(ctrl._h == 0.0), "Hidden state must be zeroed on new goal"


@pytest.mark.asyncio
async def test_set_goal_decomposes_subgoals(ctrl):
    """set_goal() must create at least one sub-goal."""
    import asyncio

    ctrl._goal_event = asyncio.Event()
    ctrl._pos_ned    = np.zeros(3, dtype=np.float32)

    await ctrl.set_goal(0.001, 0.001, 50.0)

    assert len(ctrl._sub_goals) >= 1
    assert ctrl._current_sub_idx == 0
