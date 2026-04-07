"""
OAK-D Lite DepthAI v3 pipeline manager.

Builds and manages a single DepthAI v3 pipeline with:
  - StereoDepth  (HIGH_DENSITY preset, depth aligned to RGB)
  - SpatialLocationCalculator  (5-sector horizontal obstacle scan, no NN)
  - YoloSpatialDetectionNetwork  (optional, requires blob path)

DepthAI v3 key differences from v2:
  - No explicit XLinkOut nodes; queues created directly on node outputs via
    node.output.createOutputQueue(maxSize, blocking)
  - Unified dai.node.Camera replaces ColorCamera + MonoCamera; requires .build()
  - Pipeline lifecycle: pipeline.start() (not `with dai.Device(pipeline):`)

OAK-D Lite constraints:
  - Stereo depth capped at 640×400 (OV7251 sensors)
  - Depth range: ~20 cm min, ~10 m practical max
  - Depth values: uint16, millimetres; 0 and 65535 = invalid
  - VPU: Intel Myriad X (4 TOPS, 1.4 TOPS for AI)
"""

import logging
import threading
import time
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

# 5 horizontal sectors for obstacle scanning (normalised coordinates 0.0–1.0).
# Each sector spans the middle 40% of frame height to avoid floor/ceiling noise.
_SECTORS: dict = {
    "left":         (0.00, 0.30, 0.20, 0.70),
    "center_left":  (0.20, 0.30, 0.40, 0.70),
    "center":       (0.40, 0.30, 0.60, 0.70),
    "center_right": (0.60, 0.30, 0.80, 0.70),
    "right":        (0.80, 0.30, 1.00, 0.70),
}

# YOLO anchors for yolov6n_coco_416x416 (Luxonis model zoo default)
_YOLO_ANCHORS = [10, 14, 23, 27, 37, 58, 81, 82, 135, 169, 344, 319]
_YOLO_ANCHOR_MASKS = {"side26": [1, 2, 3], "side13": [3, 4, 5]}


class OakPipeline:
    """
    DepthAI v3 pipeline for OAK-D Lite.

    Designed to be built once in app.py, started before the Gemini session
    opens, and stopped in the finally block.  Thread-safe: a mutex protects
    all queue reads so multiple async tasks can call get_* safely.
    """

    def __init__(
        self,
        fps: int = 15,
        blob_path: Optional[str] = None,
        depth_min_mm: int = 200,
        depth_max_mm: int = 8000,
    ):
        self._fps = fps
        self._blob_path = blob_path
        self._depth_min_mm = depth_min_mm
        self._depth_max_mm = depth_max_mm

        self._pipeline = None
        self._q_depth: Optional[object] = None
        self._q_slc:   Optional[object] = None
        self._q_det:   Optional[object] = None

        self._lock = threading.Lock()
        self._started = False

    # ── Lifecycle ───────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Build and start the DepthAI v3 pipeline. Raises on hardware error."""
        import depthai as dai

        pipeline = dai.Pipeline()

        # ── RGB camera (CAM_A) ────────────────────────────────────────────────
        cam_rgb = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
        cam_rgb.setFps(self._fps)

        # ── Stereo depth ──────────────────────────────────────────────────────
        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.setDefaultProfilePreset(
            dai.node.StereoDepth.PresetMode.HIGH_DENSITY
        )
        stereo.setLeftRightCheck(True)   # filter occluded pixels
        stereo.setSubpixel(False)        # disabled for speed on Myriad X
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)  # align to RGB frame

        # Raw depth output queue (1-frame FIFO, non-blocking)
        self._q_depth = stereo.depth.createOutputQueue(maxSize=1, blocking=False)

        # ── SpatialLocationCalculator (5-sector obstacle scan) ────────────────
        slc = pipeline.create(dai.node.SpatialLocationCalculator)
        stereo.depth.link(slc.inputDepth)
        slc.setWaitForConfigInput(False)

        slc_cfg = dai.SpatialLocationCalculatorConfig()
        for x0, y0, x1, y1 in _SECTORS.values():
            roi_cfg = dai.SpatialLocationCalculatorConfigData()
            roi_cfg.roi = dai.Rect(dai.Point2f(x0, y0), dai.Point2f(x1, y1))
            roi_cfg.calculationAlgorithm = dai.SpatialCalculationAlgorithm.MEDIAN
            roi_cfg.depthThresholds.lowerThreshold = self._depth_min_mm
            roi_cfg.depthThresholds.upperThreshold = self._depth_max_mm
            slc_cfg.addRoi(roi_cfg)
        slc.initialConfig = slc_cfg

        self._q_slc = slc.out.createOutputQueue(maxSize=4, blocking=False)

        # ── Optional YOLO spatial detection ───────────────────────────────────
        if self._blob_path:
            try:
                self._setup_yolo(pipeline, cam_rgb, stereo)
                logger.info(f"[OAK] YOLO detection enabled: {self._blob_path}")
            except Exception as exc:
                logger.warning(f"[OAK] YOLO setup failed ({exc}) — detection disabled")
                self._q_det = None

        # ── Start ─────────────────────────────────────────────────────────────
        pipeline.start()
        self._pipeline = pipeline
        self._started = True
        logger.info("[OAK] Pipeline started — OAK-D Lite ready")

    def stop(self) -> None:
        """Stop the pipeline and release the device."""
        if self._pipeline is not None:
            try:
                self._pipeline.stop()
            except Exception:
                pass
            self._pipeline = None
            self._started = False
            logger.info("[OAK] Pipeline stopped")

    # ── Properties ──────────────────────────────────────────────────────────────

    @property
    def available(self) -> bool:
        """True if the pipeline is running."""
        return self._started

    @property
    def detection_available(self) -> bool:
        """True if on-device YOLO detection is running."""
        return self._started and self._q_det is not None

    # ── Data accessors (thread-safe) ─────────────────────────────────────────────

    def get_depth_frame(self) -> Optional[np.ndarray]:
        """
        Return the latest depth frame as a uint16 ndarray (H×W, mm), or None.

        Values of 0 and 65535 indicate invalid / out-of-range pixels.
        """
        if not self._started or self._q_depth is None:
            return None
        with self._lock:
            msg = self._q_depth.tryGet()
            if msg is None:
                return None
            return msg.getCvFrame()

    def get_sector_distances(self) -> Optional[dict]:
        """
        Return dict mapping sector name → depth in mm from SpatialLocationCalculator.

        Returns None if no message is available yet.
        Invalid/occluded sectors have a value of 0.
        """
        if not self._started or self._q_slc is None:
            return None
        with self._lock:
            msg = self._q_slc.tryGet()
            if msg is None:
                return None
            result: dict = {}
            sector_names = list(_SECTORS.keys())
            for i, loc in enumerate(msg.getSpatialLocations()):
                if i < len(sector_names):
                    result[sector_names[i]] = loc.spatialCoordinates.z
            return result

    def get_detections(self) -> Optional[list]:
        """
        Return list of detection dicts from on-device YOLO, or None.

        Each dict: {label, confidence, x_mm, y_mm, z_mm}
        Returns None if no message is available; returns [] if frame had no detections.
        """
        if not self._started or self._q_det is None:
            return None
        with self._lock:
            msg = self._q_det.tryGet()
            if msg is None:
                return None
            return [
                {
                    "label":      d.label,
                    "confidence": round(float(d.confidence), 3),
                    "x_mm":       round(float(d.spatialCoordinates.x)),
                    "y_mm":       round(float(d.spatialCoordinates.y)),
                    "z_mm":       round(float(d.spatialCoordinates.z)),
                }
                for d in msg.detections
            ]

    # ── Private helpers ──────────────────────────────────────────────────────────

    def _setup_yolo(self, pipeline, cam_rgb, stereo) -> None:
        """
        Add YOLO spatial detection branch to an in-progress pipeline.

        Branch: RGB → ImageManip(416×416) → YoloSpatialDetectionNetwork ← depth
        """
        import depthai as dai

        # Resize RGB to 416×416 for YOLO input
        manip = pipeline.create(dai.node.ImageManip)
        manip.initialConfig.setResize(416, 416)
        manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)
        manip.setKeepAspectRatio(False)

        # Request a preview output from the RGB camera and wire it to manip
        rgb_preview = cam_rgb.requestOutput(
            (416, 416), type=dai.ImgFrame.Type.BGR888p
        )
        rgb_preview.link(manip.inputImage)

        # YOLO spatial detection network
        yolo = pipeline.create(dai.node.YoloSpatialDetectionNetwork)
        yolo.setBlobPath(self._blob_path)
        yolo.setConfidenceThreshold(0.5)
        yolo.setBoundingBoxScaleFactor(0.5)
        yolo.setDepthLowerThreshold(self._depth_min_mm)
        yolo.setDepthUpperThreshold(self._depth_max_mm)
        yolo.setNumClasses(80)
        yolo.setCoordinateSize(4)
        yolo.setAnchors(_YOLO_ANCHORS)
        yolo.setAnchorMasks(_YOLO_ANCHOR_MASKS)
        yolo.setIouThreshold(0.5)

        manip.out.link(yolo.input)
        stereo.depth.link(yolo.inputDepth)

        self._q_det = yolo.out.createOutputQueue(maxSize=4, blocking=False)
