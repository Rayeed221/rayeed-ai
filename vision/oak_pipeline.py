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

# USB reconnection policy.  The OAK-D Lite on a Raspberry Pi (drone platform)
# can lose the USB link due to: RPi bus brownouts (1.2 A shared budget vs OAK's
# 500–900 mA draw + 2 W inference spikes), cable strain on a moving frame, or
# EM interference from the ESCs.  DepthAI v3's `dai.Pipeline()` / `.start()`
# lifecycle does NOT expose `dai.Device.setMaxReconnectionAttempts()` because
# the Device is created internally.  So we implement the equivalent at the
# pipeline level: detect the drop via `pipeline.isRunning()`, stop, rebuild,
# and re-`.start()` with bounded retries + exponential backoff.
_RECONNECT_MAX_ATTEMPTS = 5
_RECONNECT_BACKOFF_BASE_S = 0.5   # 0.5, 1.0, 2.0, 4.0, 8.0 s
_RECONNECT_BACKOFF_CAP_S = 8.0


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
        pipeline, queues = self._build_graph()
        # ── Start ─────────────────────────────────────────────────────────────
        pipeline.start()
        self._pipeline = pipeline
        self._q_depth, self._q_slc, self._q_det = queues
        self._started = True
        logger.info("[OAK] Pipeline started — OAK-D Lite ready")

    def _build_graph(self):
        """
        Construct the DepthAI v3 graph and the three output queues.

        Kept separate from start() so reconnect() can rebuild the same graph
        after a USB drop without duplicating ~80 lines of node wiring.
        Returns (pipeline, (q_depth, q_slc, q_det)).
        """
        import depthai as dai

        pipeline = dai.Pipeline()

        # ── RGB camera (CAM_A) ────────────────────────────────────────────────
        # DepthAI v3: sensor fps goes through .build(sensorFps=...) — the unified
        # dai.node.Camera does not expose .setFps() (that was an old MonoCamera /
        # ColorCamera API).  See localization/vio_slam/vio_slam_runner.py for the
        # same pattern on CAM_B / CAM_C.
        cam_rgb = pipeline.create(dai.node.Camera).build(
            dai.CameraBoardSocket.CAM_A, sensorFps=self._fps
        )

        # ── Stereo depth ──────────────────────────────────────────────────────
        stereo = pipeline.create(dai.node.StereoDepth)

        # Link left and right cameras to stereo node.
        # DepthAI v3: request a concrete output at the OV7251 mono resolution
        # (640x400) via requestOutput((w, h)) — the unified dai.node.Camera has
        # no requestIspOutput(); it exposes requestOutput()/requestFullResolutionOutput().
        cam_left = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=self._fps)
        cam_right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=self._fps)
        cam_left.requestOutput((640, 400)).link(stereo.left)
        cam_right.requestOutput((640, 400)).link(stereo.right)

        stereo.setDefaultProfilePreset(
            dai.node.StereoDepth.PresetMode.DEFAULT
        )
        stereo.setLeftRightCheck(True)   # filter occluded pixels
        stereo.setSubpixel(False)        # disabled for speed on Myriad X
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)  # align to RGB frame

        # Raw depth output queue (1-frame FIFO, non-blocking)
        q_depth = stereo.depth.createOutputQueue(maxSize=1, blocking=False)

        # ── SpatialLocationCalculator (5-sector obstacle scan) ────────────────
        # DepthAI v3 removed setWaitForConfigInput(); the SLC simply uses
        # initialConfig when no runtime inputConfig message is wired in,
        # which is exactly what we want here.
        slc = pipeline.create(dai.node.SpatialLocationCalculator)
        stereo.depth.link(slc.inputDepth)

        slc_cfg = slc.initialConfig
        for x0, y0, x1, y1 in _SECTORS.values():
            roi_cfg = dai.SpatialLocationCalculatorConfigData()
            roi_cfg.roi = dai.Rect(dai.Point2f(x0, y0), dai.Point2f(x1, y1))
            roi_cfg.calculationAlgorithm = dai.SpatialLocationCalculatorAlgorithm.MEDIAN
            roi_cfg.depthThresholds.lowerThreshold = self._depth_min_mm
            roi_cfg.depthThresholds.upperThreshold = self._depth_max_mm
            slc_cfg.addROI(roi_cfg)

        q_slc = slc.out.createOutputQueue(maxSize=4, blocking=False)

        # ── Optional YOLO spatial detection ───────────────────────────────────
        q_det = None
        if self._blob_path:
            try:
                q_det = self._setup_yolo(pipeline, cam_rgb, stereo)
                logger.info(f"[OAK] YOLO detection enabled: {self._blob_path}")
            except Exception as exc:
                logger.warning(f"[OAK] YOLO setup failed ({exc}) — detection disabled")

        return pipeline, (q_depth, q_slc, q_det)

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

    def is_healthy(self) -> bool:
        """
        True if the underlying DepthAI v3 pipeline is still running.

        `pipeline.isRunning()` returns False once the USB link is lost (RPi
        brownout, cable disconnect, OAK reboot).  This is the v3-native way
        to detect a dropped connection — there is no separate Device object
        to query, since the Device is created internally by `pipeline.start()`.
        """
        return bool(self._started and self._pipeline is not None and self._pipeline.isRunning())

    def reconnect(self) -> bool:
        """
        Rebuild the pipeline graph and re-start it after a USB drop.

        Uses exponential backoff (0.5 → 1 → 2 → 4 → 8 s) with up to
        _RECONNECT_MAX_ATTEMPTS retries.  Safe to call from any thread.

        Returns True if the pipeline is running after the call, False if all
        attempts were exhausted (caller may want to surface a hard failure to
        the user or trigger a higher-level recovery).
        """
        if self._pipeline is not None and self._pipeline.isRunning():
            return True  # nothing to do

        logger.warning("[OAK] USB link lost — attempting reconnection")
        self._on_disconnect()

        # Make sure the previous pipeline object is fully torn down before
        # we try to build a new one (otherwise depthai may still hold the
        # USB endpoint and refuse to enumerate a new device).
        if self._pipeline is not None:
            try:
                self._pipeline.stop()
            except Exception:
                pass
            self._pipeline = None
        self._started = False
        self._q_depth = self._q_slc = self._q_det = None

        for attempt in range(1, _RECONNECT_MAX_ATTEMPTS + 1):
            backoff = min(_RECONNECT_BACKOFF_BASE_S * (2 ** (attempt - 1)), _RECONNECT_BACKOFF_CAP_S)
            logger.info(f"[OAK] Reconnect attempt {attempt}/{_RECONNECT_MAX_ATTEMPTS} after {backoff:.1f}s backoff")
            time.sleep(backoff)
            try:
                pipeline, queues = self._build_graph()
                pipeline.start()
                self._pipeline = pipeline
                self._q_depth, self._q_slc, self._q_det = queues
                self._started = True
                logger.info(f"[OAK] Reconnected successfully on attempt {attempt}")
                self._on_reconnected()
                return True
            except Exception as exc:
                logger.warning(f"[OAK] Reconnect attempt {attempt} failed: {exc}")

        logger.error(f"[OAK] Reconnection exhausted after {_RECONNECT_MAX_ATTEMPTS} attempts — vision offline")
        return False

    def force_reconnect(self) -> bool:
        """Public alias for reconnect() — usable from app.py or tests."""
        return self.reconnect()

    # ── Reconnect hooks (override in subclass or monkey-patch) ────────────────

    def _on_disconnect(self) -> None:
        """Called once when a USB drop is detected. Default: log only."""
        pass

    def _on_reconnected(self) -> None:
        """Called once after a successful reconnect. Default: log only."""
        pass

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

        Returns None if the pipeline is not running (caller should treat this
        as a transient "camera reconnecting" condition, not an error).
        """
        if not self.is_healthy() or self._q_depth is None:
            return None
        with self._lock:
            try:
                msg = self._q_depth.tryGet()
            except Exception as exc:
                logger.warning(f"[OAK] depth queue read failed: {exc}")
                self._started = False  # force a reconnect path on next call
                return None
            if msg is None:
                return None
            return msg.getCvFrame()

    def get_sector_distances(self) -> Optional[dict]:
        """
        Return dict mapping sector name → depth in mm from SpatialLocationCalculator.

        Returns None if no message is available yet.
        Invalid/occluded sectors have a value of 0.
        """
        if not self.is_healthy() or self._q_slc is None:
            return None
        with self._lock:
            try:
                msg = self._q_slc.tryGet()
            except Exception as exc:
                logger.warning(f"[OAK] SLC queue read failed: {exc}")
                self._started = False
                return None
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
        if not self.is_healthy() or self._q_det is None:
            return None
        with self._lock:
            try:
                msg = self._q_det.tryGet()
            except Exception as exc:
                logger.warning(f"[OAK] detection queue read failed: {exc}")
                self._started = False
                return None
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

    def _setup_yolo(self, pipeline, cam_rgb, stereo):
        """
        Add YOLO spatial detection branch to an in-progress pipeline.

        Branch: RGB → ImageManip(416×416) → YoloSpatialDetectionNetwork ← depth
        """
        import depthai as dai

        # Resize RGB to 416×416 for YOLO input
        manip = pipeline.create(dai.node.ImageManip)
        manip.initialConfig.setOutputSize(416, 416)
        manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)

        # Request a preview output from the RGB camera and wire it to manip
        rgb_preview = cam_rgb.requestOutput(
            (416, 416), type=dai.ImgFrame.Type.BGR888p
        )
        rgb_preview.link(manip.inputImage)

        # YOLO spatial detection network
        yolo = pipeline.create(dai.node.SpatialDetectionNetwork)
        yolo.setBlobPath(self._blob_path)
        yolo.setConfidenceThreshold(0.5)
        yolo.setBoundingBoxScaleFactor(0.5)
        yolo.setDepthLowerThreshold(self._depth_min_mm)
        yolo.setDepthUpperThreshold(self._depth_max_mm)

        manip.out.link(yolo.input)
        stereo.depth.link(yolo.inputDepth)

        return yolo.out.createOutputQueue(maxSize=4, blocking=False)
