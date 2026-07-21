"""
Tests for the vision/ module.

These tests cover the pure-numpy helpers in `vision/depth_analyzer.py` and
the label lookup.  The OakPipeline + VisionTool integration (including the
USB-drop / reconnect path that matters on a Raspberry Pi drone) is covered
by tests/test_depthai/test_oak_pipeline_reconnect.py using a fake `dai`
module — see that file for the reconnect / is_healthy coverage.
"""

import numpy as np

from vision.depth_analyzer import (
    analyze_depth_grid,
    check_landing_zone,
    label_name,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_depth(h: int = 400, w: int = 640, fill_mm: int = 2000) -> np.ndarray:
    """Return a uniform uint16 depth array."""
    return np.full((h, w), fill_mm, dtype=np.uint16)


def _make_noisy_depth(h: int = 400, w: int = 640, seed: int = 42) -> np.ndarray:
    """Return a depth array with significant variance (uneven terrain)."""
    rng = np.random.default_rng(seed)
    base = 2000
    noise = rng.integers(-600, 600, size=(h, w))
    return np.clip(base + noise, 200, 8000).astype(np.uint16)


def _make_invalid_depth(h: int = 400, w: int = 640) -> np.ndarray:
    """Return an all-zero (all-invalid) depth array."""
    return np.zeros((h, w), dtype=np.uint16)


# ── label_name ────────────────────────────────────────────────────────────────

def test_label_name_known():
    assert label_name(0) == "person"
    assert label_name(2) == "car"
    assert label_name(79) == "toothbrush"


def test_label_name_unknown():
    result = label_name(999)
    assert result.startswith("class_")


# ── analyze_depth_grid ────────────────────────────────────────────────────────

def test_analyze_depth_grid_returns_9_cells():
    depth = _make_depth()
    result = analyze_depth_grid(depth)
    assert len(result["grid"]) == 9


def test_analyze_depth_grid_cell_keys():
    depth = _make_depth()
    result = analyze_depth_grid(depth)
    cell = result["grid"][0]
    assert "name" in cell
    assert "mean_m" in cell
    assert "min_m" in cell
    assert "coverage_pct" in cell


def test_analyze_depth_grid_uniform_values():
    depth = _make_depth(fill_mm=3000)
    result = analyze_depth_grid(depth)
    for cell in result["grid"]:
        assert abs(cell["mean_m"] - 3.0) < 0.01
        assert abs(cell["min_m"] - 3.0) < 0.01
        assert cell["coverage_pct"] == 100.0


def test_analyze_depth_grid_nearest_m():
    depth = _make_depth(fill_mm=2000)
    result = analyze_depth_grid(depth)
    assert result["nearest_m"] == 2.0


def test_analyze_depth_grid_coverage_full():
    depth = _make_depth(fill_mm=1000)
    result = analyze_depth_grid(depth)
    assert result["coverage_pct"] == 100.0


def test_analyze_depth_grid_all_invalid():
    depth = _make_invalid_depth()
    result = analyze_depth_grid(depth)
    assert result["nearest_m"] is None
    assert result["coverage_pct"] == 0.0
    for cell in result["grid"]:
        assert cell["coverage_pct"] == 0.0
        assert cell["mean_m"] == 0.0


def test_analyze_depth_grid_filters_close_pixels():
    # Pixels at 100 mm should be excluded (below min_mm=200)
    depth = np.full((400, 640), 100, dtype=np.uint16)
    result = analyze_depth_grid(depth, min_mm=200)
    assert result["nearest_m"] is None
    assert result["coverage_pct"] == 0.0


def test_analyze_depth_grid_cell_names():
    depth = _make_depth()
    result = analyze_depth_grid(depth)
    names = [c["name"] for c in result["grid"]]
    assert "top_left" in names
    assert "mid_center" in names
    assert "bot_right" in names


# ── check_landing_zone ────────────────────────────────────────────────────────

def test_check_landing_zone_flat_safe():
    depth = _make_depth(fill_mm=2000)
    result = check_landing_zone(depth)
    assert result["safe"] is True
    assert result["std_m"] == 0.0
    assert result["reason"] == "flat"
    assert result["coverage_pct"] == 100.0
    assert abs(result["mean_m"] - 2.0) < 0.01


def test_check_landing_zone_uneven_unsafe():
    depth = _make_noisy_depth()  # high variance
    result = check_landing_zone(depth, flatness_threshold_m=0.1)
    assert result["safe"] is False
    assert "uneven" in result["reason"]
    assert result["std_m"] is not None
    assert result["std_m"] > 0.1


def test_check_landing_zone_insufficient_coverage():
    depth = _make_invalid_depth()
    result = check_landing_zone(depth)
    assert result["safe"] is False
    assert "coverage" in result["reason"]
    assert result["std_m"] is None
    assert result["mean_m"] is None


def test_check_landing_zone_coverage_pct_populated():
    depth = _make_depth(fill_mm=1500)
    result = check_landing_zone(depth)
    assert result["coverage_pct"] == 100.0


# ── VisionTool (with real OakPipeline) ──────────────────────────────────────
#
# NOTE: Previous versions of this file used a `_MockPipeline` stub to test
# VisionTool.  That mock only stubbed the three queue getters and so could
# never exercise the USB-drop / reconnect path that matters on a Raspberry Pi
# drone platform.  The real-pipeline tests now live in
# tests/test_depthai/test_oak_pipeline_reconnect.py and use a fake `dai`
# module injected via sys.modules so they run without an OAK-D Lite attached.
# VisionTool's behaviour with the real pipeline is covered indirectly by
# those tests, since VisionTool calls the same OakPipeline methods.
