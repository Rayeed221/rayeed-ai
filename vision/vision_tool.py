"""
VisionTool — bridges OakPipeline to the tool dispatcher.

Provides synchronous execute(tool_name, args) which is called via
asyncio.to_thread() in the dispatcher so blocking frame reads don't
stall the event loop.

Three tools:
  vision_obstacle_check  — 5-sector SLC scan (no NN, fastest)
  vision_depth_snapshot  — 3×3 grid stats + landing zone assessment
  vision_detect_objects  — on-device YOLO spatial detection (needs blob)
"""

import logging
import time
from typing import TYPE_CHECKING

from vision.depth_analyzer import analyze_depth_grid, check_landing_zone, label_name

if TYPE_CHECKING:
    from vision.oak_pipeline import OakPipeline

logger = logging.getLogger(__name__)

# How long to wait for a fresh frame before giving up
_FRAME_TIMEOUT_S = 1.0
_POLL_INTERVAL_S = 0.05

# Obstacle clearance threshold: sectors closer than this are flagged
_OBSTACLE_THRESHOLD_MM = 1500  # 1.5 m


class VisionTool:
    """Synchronous vision tool executor backed by OakPipeline."""

    def __init__(self, pipeline: "OakPipeline"):
        self._pipeline = pipeline

    # ── Dispatcher entry point ───────────────────────────────────────────────────

    def execute(self, tool_name: str, args: dict) -> dict:
        """Route tool_name to the appropriate handler. Returns a plain dict."""
        if not self._pipeline.available:
            return {"error": "OAK-D camera not available"}

        if tool_name == "vision_obstacle_check":
            return self._obstacle_check(args)
        if tool_name == "vision_depth_snapshot":
            return self._depth_snapshot(args)
        if tool_name == "vision_detect_objects":
            return self._detect_objects(args)

        return {"error": f"Unknown vision tool: {tool_name}"}

    # ── Tool handlers ────────────────────────────────────────────────────────────

    def _obstacle_check(self, args: dict) -> dict:
        """
        Query SpatialLocationCalculator for the 5 horizontal sectors and
        report distances in metres plus a 'clear' flag.

        Returns:
            sectors_m:          {sector_name: distance_m} — only valid sectors
            nearest_sector:     name of closest sector (None if all clear/invalid)
            nearest_distance_m: distance to nearest obstacle in metres
            clear:              True if no obstacle within OBSTACLE_THRESHOLD
        """
        sectors = self._wait_for(self._pipeline.get_sector_distances)
        if sectors is None:
            return {"error": "No depth data from SpatialLocationCalculator — camera warming up?"}

        # z_mm == 0 means SLC returned no valid depth for that sector
        valid = {k: v for k, v in sectors.items() if v > 0}

        if not valid:
            return {
                "sectors_m":          {},
                "nearest_sector":     None,
                "nearest_distance_m": None,
                "clear":              True,
            }

        nearest_sector = min(valid, key=lambda k: valid[k])
        nearest_mm = valid[nearest_sector]

        return {
            "sectors_m":          {k: round(v / 1000.0, 2) for k, v in valid.items()},
            "nearest_sector":     nearest_sector,
            "nearest_distance_m": round(nearest_mm / 1000.0, 2),
            "clear":              nearest_mm > _OBSTACLE_THRESHOLD_MM,
        }

    def _depth_snapshot(self, args: dict) -> dict:
        """
        Capture a depth frame and return:
          - 3×3 grid per-cell statistics (mean_m, min_m, coverage_pct)
          - global nearest valid distance
          - landing zone flatness assessment

        Returns:
            frame_shape:        [H, W]
            grid:               list of 9 cell dicts
            nearest_m:          global nearest valid distance in metres
            depth_coverage_pct: fraction of frame with valid depth
            landing_zone:       {safe, reason, std_m, coverage_pct, mean_m}
        """
        depth = self._wait_for(self._pipeline.get_depth_frame)
        if depth is None:
            return {"error": "No depth frame available — camera warming up?"}

        grid_result = analyze_depth_grid(depth)
        landing_result = check_landing_zone(depth)

        return {
            "frame_shape":         list(depth.shape),
            "grid":                grid_result["grid"],
            "nearest_m":           grid_result["nearest_m"],
            "depth_coverage_pct":  grid_result["coverage_pct"],
            "landing_zone":        landing_result,
        }

    def _detect_objects(self, args: dict) -> dict:
        """
        Run on-device YOLO and return spatial detections with 3D coordinates.

        Args (optional):
            min_confidence: float 0.0–1.0, default 0.5

        Returns:
            count:      number of detections above threshold
            detections: list of {label, label_name, confidence, x_mm, y_mm, z_mm}
        """
        if not self._pipeline.detection_available:
            return {"error": "YOLO detection not available — blob not loaded"}

        detections = self._wait_for(self._pipeline.get_detections)
        if detections is None:
            return {"error": "No detections frame available — camera warming up?"}

        min_conf = float(args.get("min_confidence", 0.5))
        labelled = [
            {**d, "label_name": label_name(d["label"])}
            for d in detections
            if d["confidence"] >= min_conf
        ]

        return {
            "count":      len(labelled),
            "detections": labelled,
        }

    # ── Helpers ──────────────────────────────────────────────────────────────────

    def _wait_for(self, fn):
        """
        Poll fn() until it returns a non-None result or _FRAME_TIMEOUT_S elapses.
        Accounts for pipeline warm-up (first few frames may not yet be available).
        """
        deadline = time.monotonic() + _FRAME_TIMEOUT_S
        while time.monotonic() < deadline:
            result = fn()
            if result is not None:
                return result
            time.sleep(_POLL_INTERVAL_S)
        return None
