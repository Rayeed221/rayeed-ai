"""
Numpy-based depth frame analysis utilities (no NN required).

Operates directly on uint16 depth arrays (mm units) from OAK-D Lite.
"""

import numpy as np

# COCO 80-class label names (for label_id → name lookup)
COCO_LABELS = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
    "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
    "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv",
    "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush",
]

# 3×3 cell names (row-major)
_CELL_NAMES = [
    ["top_left",    "top_center",    "top_right"],
    ["mid_left",    "mid_center",    "mid_right"],
    ["bot_left",    "bot_center",    "bot_right"],
]


def label_name(label_id: int) -> str:
    """Return COCO class name for a label index."""
    if 0 <= label_id < len(COCO_LABELS):
        return COCO_LABELS[label_id]
    return f"class_{label_id}"


def analyze_depth_grid(
    depth: np.ndarray,
    rows: int = 3,
    cols: int = 3,
    min_mm: int = 200,
    max_mm: int = 8000,
) -> dict:
    """
    Divide depth frame into rows×cols grid, return per-cell statistics.

    Args:
        depth:   uint16 ndarray (H, W), values in mm; 0 and 65535 = invalid
        rows:    grid rows
        cols:    grid columns
        min_mm:  ignore pixels closer than this (mm)
        max_mm:  ignore pixels farther than this (mm)

    Returns dict:
        grid:          list of {name, mean_m, min_m, coverage_pct}
        nearest_m:     global nearest valid distance in metres (None if no valid pixels)
        coverage_pct:  percentage of frame with valid depth
    """
    h, w = depth.shape
    valid_mask = (depth > min_mm) & (depth < max_mm)
    total_valid = int(valid_mask.sum())
    total_pixels = h * w

    cell_h = h // rows
    cell_w = w // cols

    grid = []
    for r in range(rows):
        for c in range(cols):
            y0, y1 = r * cell_h, (r + 1) * cell_h
            x0, x1 = c * cell_w, (c + 1) * cell_w
            cell = depth[y0:y1, x0:x1]
            cell_valid = valid_mask[y0:y1, x0:x1]
            n_valid = int(cell_valid.sum())
            coverage = n_valid / max(cell.size, 1)
            if n_valid > 0:
                mean_mm = float(cell[cell_valid].mean())
                min_mm_cell = float(cell[cell_valid].min())
            else:
                mean_mm = 0.0
                min_mm_cell = 0.0
            name = (
                _CELL_NAMES[r][c]
                if r < len(_CELL_NAMES) and c < len(_CELL_NAMES[r])
                else f"cell_{r}_{c}"
            )
            grid.append({
                "name":         name,
                "mean_m":       round(mean_mm / 1000.0, 2),
                "min_m":        round(min_mm_cell / 1000.0, 2),
                "coverage_pct": round(coverage * 100, 1),
            })

    valid_pixels = depth[valid_mask]
    nearest_m = round(float(valid_pixels.min()) / 1000.0, 2) if len(valid_pixels) > 0 else None
    global_coverage = round(total_valid / max(total_pixels, 1) * 100, 1)

    return {
        "grid":         grid,
        "nearest_m":    nearest_m,
        "coverage_pct": global_coverage,
    }


def check_landing_zone(
    depth: np.ndarray,
    center_fraction: float = 0.4,
    flatness_threshold_m: float = 0.3,
    min_coverage: float = 0.6,
    min_mm: int = 200,
    max_mm: int = 8000,
) -> dict:
    """
    Assess the centre of the depth frame for landing suitability.

    The zone is a square covering `center_fraction` of both axes, centred
    in the frame.  Landing is considered safe if the zone has sufficient
    valid depth coverage and low depth variance (flat surface).

    Returns dict:
        safe:         bool
        reason:       human-readable explanation
        std_m:        depth std-dev within zone in metres (None if uncovered)
        coverage_pct: percentage of zone with valid depth
        mean_m:       mean depth of zone in metres (None if uncovered)
    """
    h, w = depth.shape
    y0 = int(h * (0.5 - center_fraction / 2))
    y1 = int(h * (0.5 + center_fraction / 2))
    x0 = int(w * (0.5 - center_fraction / 2))
    x1 = int(w * (0.5 + center_fraction / 2))

    zone = depth[y0:y1, x0:x1]
    valid_mask = (zone > min_mm) & (zone < max_mm)
    n_valid = int(valid_mask.sum())
    coverage = n_valid / max(zone.size, 1)

    if coverage < min_coverage:
        return {
            "safe":         False,
            "reason":       (
                f"insufficient depth coverage "
                f"({coverage * 100:.0f}% < {min_coverage * 100:.0f}%)"
            ),
            "std_m":        None,
            "coverage_pct": round(coverage * 100, 1),
            "mean_m":       None,
        }

    valid_depths = zone[valid_mask].astype(np.float64)
    std_mm = float(valid_depths.std())
    mean_mm = float(valid_depths.mean())
    safe = std_mm < (flatness_threshold_m * 1000)

    return {
        "safe":         safe,
        "reason":       (
            "flat"
            if safe
            else f"uneven terrain (std={std_mm / 1000:.2f}m > {flatness_threshold_m}m)"
        ),
        "std_m":        round(std_mm / 1000.0, 3),
        "coverage_pct": round(coverage * 100, 1),
        "mean_m":       round(mean_mm / 1000.0, 2),
    }
