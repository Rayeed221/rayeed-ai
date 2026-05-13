"""
VIOSLAMRunner — autonomous VIO + SLAM background task.

Owns its own DepthAI v3 pipeline (RTABMapVIO + RTABMapSLAM) on the OAK-D
Lite.  Publishes:

  - VIOPose      — high-rate 6-DOF pose; pushed into PoseCache every tick
  - SLAMSnapshot — aggregate occupancy-grid state
  - LiveOccupancyGrid — 3D obstacle grid (accessed read-only by safety_policy)

Mirrors vision/avoidance/dronet_runner.py 1:1:
  - lazy `import depthai` inside run() — non-fatal if missing
  - all blocking DepthAI calls wrapped in `await asyncio.to_thread(...)`
  - thread-safe state behind a single lock
  - cooperative cancel via CancelledError → finally → pipeline.stop()

HARDWARE CONSTRAINT: the OAK-D Lite's Myriad X cannot host RTABMapSLAM +
SpatialLocationCalculator + YOLO simultaneously.  Enable only one of
{VISION_ENABLED, VIOSLAM_ENABLED} per OAK-D unit.
"""

import asyncio
import locale
import logging
import math
import threading
import time
from typing import Optional

import numpy as np

from localization.vio_slam.occupancy_grid import LiveOccupancyGrid
from localization.vio_slam.rtabmap_params import SLAM_PARAMS, VIO_PARAMS
from localization.vio_slam.slam_state import SLAMSnapshot, VIOPose

logger = logging.getLogger(__name__)

# RTABMap parses numeric params via the C locale (".") regardless of system
# locale.  Force it at import time so a German/French/etc.  locale ("," as
# decimal separator) does not silently corrupt the param dicts.
try:
    locale.setlocale(locale.LC_NUMERIC, "C")
except locale.Error:
    pass


class VIOSLAMRunner:
    """
    Asyncio background task that drives the OAK-D Lite VIO+SLAM pipeline.

    Public API (all thread-safe):
        get_pose()          → latest VIOPose or None
        get_snapshot()      → latest SLAMSnapshot or None
        get_occupancy_grid()→ live grid reference (read-only contract)
        run()               → coroutine; add to background_tasks in app.py
    """

    # How many run() iterations between decay ticks (10 iterations ≈ 0.33 s at 30 fps)
    DECAY_EVERY_N = 10
    # Stereo capture resolution — matches the exploration script
    _CAPTURE_WIDTH = 640
    _CAPTURE_HEIGHT = 400

    def __init__(
        self,
        *,
        db_path: str,
        load_db: bool,
        fps: int,
        slam_hz: float,
        occ_cell_size: float,
        pose_cache,
    ):
        self._db_path        = db_path
        self._load_db        = load_db
        self._fps            = fps
        self._slam_hz        = slam_hz
        self._pose_cache     = pose_cache
        self._occ_grid       = LiveOccupancyGrid(cell_size=occ_cell_size)

        self._lock = threading.Lock()
        self._pose:     Optional[VIOPose]      = None
        self._snapshot: Optional[SLAMSnapshot] = None

    # ── Public API ────────────────────────────────────────────────────────────

    def get_pose(self) -> Optional[VIOPose]:
        with self._lock:
            return self._pose

    def get_snapshot(self) -> Optional[SLAMSnapshot]:
        with self._lock:
            return self._snapshot

    def get_occupancy_grid(self) -> LiveOccupancyGrid:
        """Read-only contract: callers MUST NOT mutate the returned grid."""
        return self._occ_grid

    # ── Main coroutine ────────────────────────────────────────────────────────

    async def run(self) -> None:
        """20–30 Hz VIO + SLAM loop.  Non-fatal on any setup failure."""
        try:
            import depthai  # noqa: F401
        except ImportError:
            logger.warning("[VIOSLAM] depthai not installed — VIO/SLAM loop disabled")
            return

        logger.info(
            f"[VIOSLAM] Starting — fps={self._fps} slam_hz={self._slam_hz} "
            f"db={self._db_path} load_db={self._load_db}"
        )

        try:
            pipeline, queues = await asyncio.to_thread(self._build_pipeline)
        except Exception as exc:
            logger.warning(f"[VIOSLAM] Pipeline build failed: {exc} — VIO/SLAM loop disabled")
            return

        q_vio_transform, q_slam_transform, q_obstacle_pcl = queues
        period_s = 1.0 / max(1, self._fps)
        iter_count = 0

        try:
            while pipeline.isRunning():
                # ── 1. Pose update — prefer SLAM (loop-closed); fall back to VIO ──
                pose_msg = q_slam_transform.tryGet()
                pose_source = "slam"
                if pose_msg is None:
                    pose_msg = q_vio_transform.tryGet()
                    pose_source = "vio"

                if pose_msg is not None:
                    vp = self._transform_to_vio_pose(pose_msg, source=pose_source)
                    with self._lock:
                        self._pose = vp
                    self._pose_cache.update_from_vio(vp)

                # ── 2. Obstacle cloud → occupancy grid → snapshot ──
                pcl_msg = q_obstacle_pcl.tryGet()
                if pcl_msg is not None:
                    pts = self._pcl_to_numpy(pcl_msg)
                    if pts.shape[0] > 0:
                        # Subsample if huge — keeps the grid insertion cheap
                        if pts.shape[0] > 5000:
                            idx = np.random.choice(pts.shape[0], 5000, replace=False)
                            pts = pts[idx]
                        self._occ_grid.insert_obstacle_points(pts, inflate_cells=2)
                    snapshot = SLAMSnapshot(
                        occupied_cells=self._occ_grid.occupied_count(),
                        grid_origin_xy=(self._occ_grid.origin_x, self._occ_grid.origin_y),
                        timestamp=time.monotonic(),
                    )
                    with self._lock:
                        self._snapshot = snapshot

                # ── 3. Periodic decay so stale obstacles fade ──
                iter_count += 1
                if iter_count % self.DECAY_EVERY_N == 0:
                    self._occ_grid.decay(amount=1)

                await asyncio.sleep(period_s)

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.exception(f"[VIOSLAM] Runtime error: {exc}")
        finally:
            try:
                pipeline.stop()
            except Exception:
                pass
            logger.info("[VIOSLAM] Loop stopped (SLAM DB auto-saved on close)")

    # ── Pipeline construction ─────────────────────────────────────────────────

    def _build_pipeline(self):
        """
        Build and start the DepthAI v3 pipeline per the spec in CLAUDE.md.

        Returns (pipeline, (q_vio_transform, q_slam_transform, q_obstacle_pcl)).
        Runs in a worker thread (called via asyncio.to_thread).
        """
        import depthai as dai

        p = dai.Pipeline()

        # ── Cameras (mono left/right via unified Camera.build) ────────────────
        cam_left  = p.create(dai.node.Camera).build(
            dai.CameraBoardSocket.CAM_B, sensorFps=self._fps
        )
        cam_right = p.create(dai.node.Camera).build(
            dai.CameraBoardSocket.CAM_C, sensorFps=self._fps
        )

        # ── IMU ────────────────────────────────────────────────────────────────
        imu = p.create(dai.node.IMU)
        imu.enableIMUSensor(
            [dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200
        )
        imu.setBatchReportThreshold(1)
        imu.setMaxBatchReports(10)

        # ── Stereo depth ──────────────────────────────────────────────────────
        stereo = p.create(dai.node.StereoDepth)
        stereo.setExtendedDisparity(False)
        stereo.setLeftRightCheck(True)
        stereo.setRectifyEdgeFillColor(0)
        stereo.enableDistortionCorrection(True)
        stereo.initialConfig.setLeftRightCheckThreshold(10)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)

        cam_left.requestOutput((self._CAPTURE_WIDTH, self._CAPTURE_HEIGHT)).link(stereo.left)
        cam_right.requestOutput((self._CAPTURE_WIDTH, self._CAPTURE_HEIGHT)).link(stereo.right)

        # ── Feature tracker ───────────────────────────────────────────────────
        tracker = p.create(dai.node.FeatureTracker)
        tracker.setHardwareResources(1, 2)
        tracker.initialConfig.setCornerDetector(
            dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS
        )
        tracker.initialConfig.setNumTargetFeatures(1000)
        tracker.initialConfig.setMotionEstimator(False)
        tracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

        stereo.rectifiedLeft.link(tracker.inputImage)

        # ── VIO node ──────────────────────────────────────────────────────────
        vio = p.create(dai.node.RTABMapVIO)
        vio.setUseFeatures(True)
        vio.setParams(VIO_PARAMS)

        tracker.passthroughInputImage.link(vio.rect)
        stereo.depth.link(vio.depth)
        tracker.outputFeatures.link(vio.features)
        imu.out.link(vio.imu)

        # ── SLAM node ─────────────────────────────────────────────────────────
        slam = p.create(dai.node.RTABMapSLAM)
        slam.setFreq(self._slam_hz)
        slam.setAlphaScaling(-1.0)
        slam.setDatabasePath(self._db_path)
        slam.setLoadDatabaseOnStart(self._load_db)
        slam.setSaveDatabaseOnClose(True)
        slam.setSaveDatabasePeriodically(True)
        slam.setSaveDatabasePeriod(60.0)
        slam.setPublishGrid(True)
        slam.setPublishObstacleCloud(True)
        slam.setParams(SLAM_PARAMS)

        vio.transform.link(slam.odom)
        vio.passthroughRect.link(slam.rect)
        vio.passthroughDepth.link(slam.depth)

        # ── Output queues ─────────────────────────────────────────────────────
        q_vio_transform  = vio.transform.createOutputQueue(maxSize=1, blocking=False)
        q_slam_transform = slam.transform.createOutputQueue(maxSize=1, blocking=False)
        q_obstacle_pcl   = slam.obstaclePCL.createOutputQueue(maxSize=1, blocking=False)

        p.start()
        logger.info("[VIOSLAM] DepthAI pipeline started")
        return p, (q_vio_transform, q_slam_transform, q_obstacle_pcl)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _transform_to_vio_pose(self, transform_msg, source: str) -> VIOPose:
        """Convert a DepthAI TransformData message into a VIOPose dataclass."""
        t = transform_msg.getTranslation()
        q = transform_msg.getQuaternion()
        heading = self._quat_to_heading_deg(q.qw, q.qx, q.qy, q.qz)
        return VIOPose(
            x=float(t.x), y=float(t.y), z=float(t.z),
            qw=float(q.qw), qx=float(q.qx), qy=float(q.qy), qz=float(q.qz),
            heading_deg=heading,
            source=source,
            timestamp=time.monotonic(),
        )

    @staticmethod
    def _pcl_to_numpy(pcl_msg) -> np.ndarray:
        """Convert DepthAI PointCloudData to an Nx3 ndarray.  Empty → (0, 3)."""
        points = pcl_msg.getPoints()
        if len(points) == 0:
            return np.empty((0, 3), dtype=np.float32)
        arr = np.asarray(points, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr.reshape(-1, 3)
        return arr

    @staticmethod
    def _quat_to_heading_deg(qw: float, qx: float, qy: float, qz: float) -> float:
        """Extract yaw (Z-axis rotation) from quaternion, returned in [0, 360)."""
        siny_cosp = 2.0 * (qw * qz + qx * qy)
        cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
        heading = math.degrees(math.atan2(siny_cosp, cosy_cosp))
        return heading % 360.0
