"""
Tests for the vision/ module.

All tests are synchronous and run without hardware by mocking OakPipeline
and providing synthetic numpy depth arrays.  No depthai installation needed.
"""

import numpy as np
import pytest

from vision.depth_analyzer import (
    analyze_depth_grid,
    check_landing_zone,
    label_name,
)
from vision.vision_tool import VisionTool


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


# ── VisionTool (mocked pipeline) ─────────────────────────────────────────────

class _MockPipeline:
    """Minimal mock for OakPipeline used in VisionTool tests."""

    def __init__(
        self,
        depth: np.ndarray = None,
        sectors: dict = None,
        detections: list = None,
        detection_available: bool = True,
    ):
        self._depth = depth if depth is not None else _make_depth()
        self._sectors = sectors
        self._detections = detections
        self.available = True
        self.detection_available = detection_available

    def get_depth_frame(self):
        return self._depth

    def get_sector_distances(self):
        return self._sectors

    def get_detections(self):
        return self._detections


@pytest.fixture
def tool_uniform():
    pipeline = _MockPipeline(
        depth=_make_depth(fill_mm=2000),
        sectors={
            "left": 3000.0, "center_left": 2800.0,
            "center": 1200.0, "center_right": 2500.0, "right": 3100.0,
        },
        detections=[
            {"label": 0, "confidence": 0.92, "x_mm": 50, "y_mm": -10, "z_mm": 1200},
            {"label": 2, "confidence": 0.45, "x_mm": 200, "y_mm": 30, "z_mm": 3500},
        ],
    )
    return VisionTool(pipeline)


@pytest.fixture
def tool_no_camera():
    pipeline = _MockPipeline()
    pipeline.available = False
    return VisionTool(pipeline)


# ── vision_obstacle_check ─────────────────────────────────────────────────────

def test_obstacle_check_returns_expected_keys(tool_uniform):
    result = tool_uniform.execute("vision_obstacle_check", {})
    assert "sectors" in result           # renamed from sectors_m (now holds enriched dicts)
    assert "nearest_sector" in result
    assert "nearest_distance_m" in result
    assert "clear" in result


def test_obstacle_check_nearest_sector(tool_uniform):
    result = tool_uniform.execute("vision_obstacle_check", {})
    assert result["nearest_sector"] == "center"
    assert result["nearest_distance_m"] == 1.2
    assert result["clear"] is False  # 1200 mm < 1500 mm threshold → obstacle detected


def test_obstacle_check_clear_flag():
    pipeline = _MockPipeline(
        sectors={"left": 4000.0, "center_left": 5000.0, "center": 6000.0,
                 "center_right": 5500.0, "right": 4500.0},
    )
    vt = VisionTool(pipeline)
    result = vt.execute("vision_obstacle_check", {})
    assert result["clear"] is True


def test_obstacle_check_not_clear():
    pipeline = _MockPipeline(
        sectors={"left": 500.0, "center_left": 300.0, "center": 200.0,
                 "center_right": 400.0, "right": 600.0},
    )
    vt = VisionTool(pipeline)
    result = vt.execute("vision_obstacle_check", {})
    assert result["clear"] is False


def test_obstacle_check_all_zero_sectors():
    pipeline = _MockPipeline(
        sectors={"left": 0, "center_left": 0, "center": 0,
                 "center_right": 0, "right": 0},
    )
    vt = VisionTool(pipeline)
    result = vt.execute("vision_obstacle_check", {})
    assert result["clear"] is True
    assert result["nearest_sector"] is None


def test_obstacle_check_camera_unavailable(tool_no_camera):
    result = tool_no_camera.execute("vision_obstacle_check", {})
    assert "error" in result


def test_obstacle_check_no_slc_data():
    pipeline = _MockPipeline(sectors=None)
    vt = VisionTool(pipeline)
    result = vt.execute("vision_obstacle_check", {})
    assert "error" in result


# ── vision_depth_snapshot ─────────────────────────────────────────────────────

def test_depth_snapshot_returns_expected_keys(tool_uniform):
    result = tool_uniform.execute("vision_depth_snapshot", {})
    assert "frame_shape" in result
    assert "grid" in result
    assert "nearest_m" in result
    assert "depth_coverage_pct" in result
    assert "landing_zone" in result


def test_depth_snapshot_frame_shape(tool_uniform):
    result = tool_uniform.execute("vision_depth_snapshot", {})
    assert result["frame_shape"] == [400, 640]


def test_depth_snapshot_grid_length(tool_uniform):
    result = tool_uniform.execute("vision_depth_snapshot", {})
    assert len(result["grid"]) == 9


def test_depth_snapshot_landing_zone_keys(tool_uniform):
    result = tool_uniform.execute("vision_depth_snapshot", {})
    lz = result["landing_zone"]
    assert "safe" in lz
    assert "reason" in lz
    assert "std_m" in lz
    assert "coverage_pct" in lz
    assert "mean_m" in lz


def test_depth_snapshot_flat_is_safe(tool_uniform):
    result = tool_uniform.execute("vision_depth_snapshot", {})
    assert result["landing_zone"]["safe"] is True


def test_depth_snapshot_no_depth():
    pipeline = _MockPipeline(depth=None)
    pipeline.get_depth_frame = lambda: None
    vt = VisionTool(pipeline)
    result = vt.execute("vision_depth_snapshot", {})
    assert "error" in result


# ── vision_detect_objects ─────────────────────────────────────────────────────

def test_detect_objects_returns_expected_keys(tool_uniform):
    result = tool_uniform.execute("vision_detect_objects", {})
    assert "count" in result
    assert "detections" in result


def test_detect_objects_count(tool_uniform):
    # Default min_confidence=0.5; only the 0.92-confidence detection passes
    result = tool_uniform.execute("vision_detect_objects", {})
    assert result["count"] == 1
    assert len(result["detections"]) == 1


def test_detect_objects_label_name(tool_uniform):
    result = tool_uniform.execute("vision_detect_objects", {})
    det = result["detections"][0]
    assert det["label_name"] == "person"
    assert det["label"] == 0
    assert det["confidence"] == 0.92


def test_detect_objects_spatial_coords(tool_uniform):
    result = tool_uniform.execute("vision_detect_objects", {})
    det = result["detections"][0]
    assert "x_mm" in det
    assert "y_mm" in det
    assert "z_mm" in det
    assert det["z_mm"] == 1200


def test_detect_objects_min_confidence_filter(tool_uniform):
    # Lower threshold — both detections should pass
    result = tool_uniform.execute("vision_detect_objects", {"min_confidence": 0.4})
    assert result["count"] == 2


def test_detect_objects_high_threshold_filters_all(tool_uniform):
    result = tool_uniform.execute("vision_detect_objects", {"min_confidence": 0.99})
    assert result["count"] == 0


def test_detect_objects_no_blob():
    pipeline = _MockPipeline(detection_available=False)
    vt = VisionTool(pipeline)
    result = vt.execute("vision_detect_objects", {})
    assert "error" in result


def test_detect_objects_empty_frame():
    pipeline = _MockPipeline(detections=[])
    vt = VisionTool(pipeline)
    result = vt.execute("vision_detect_objects", {})
    assert result["count"] == 0
    assert result["detections"] == []


def test_detect_objects_camera_unavailable(tool_no_camera):
    result = tool_no_camera.execute("vision_detect_objects", {})
    assert "error" in result


# ── Unknown tool ──────────────────────────────────────────────────────────────

def test_unknown_tool_returns_error():
    vt = VisionTool(_MockPipeline())
    result = vt.execute("vision_fly_to_moon", {})
    assert "error" in result
