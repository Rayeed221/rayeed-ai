#!/usr/bin/env python3
"""
SpatialLocationCalculator + RTABMap SLAM → MAVLink 3D Obstacle Avoidance
=========================================================================

Combines two DepthAI on-device features for comprehensive avoidance:

1. SpatialLocationCalculator: Dense multi-ROI grid covering the full FOV
   → Gives hardware-accelerated XYZ per sector (runs on VPU, not host)
   → Feeds OBSTACLE_DISTANCE (72-bin 2D) + OBSTACLE_DISTANCE_3D (per-sector)

2. RTABMap SLAM occupancyGrid + obstaclePCL:
   → Gives 360° map-based coverage (includes areas behind the camera)
   → Fills the "blind" bins in OBSTACLE_DISTANCE that the camera can't see
   → Feeds dynamic fence upload for Dijkstra path planning

Architecture Overview:
─────────────────────────────────────────────────────────────────────

 OAK-D Lite (DepthAI v3 Pipeline)
 ┌──────────────────────────────────────────────────────────────────┐
 │                                                                  │
 │  ┌──────────┐   ┌────────────┐   ┌──────────────────────┐        │
 │  │ Left Cam │──▶│            │──▶│ SpatialLocation      │──out──┼──▶ Host
 │  │ Right Cam│──▶│ StereoDepth│──▶│ Calculator (N ROIs)  │       │
 │  └──────────┘   │            │   └──────────────────────┘       │
 │                  │            │                                  │
 │  ┌──────────┐   │            │   ┌────────────┐  ┌───────────┐  │
 │  │   IMU    │──▶│            │──▶│ RTABMapVIO │─▶│RTABMapSLAM│──┼──▶ Host
 │  └──────────┘   │            │   │            │  │  occGrid  │  │
 │                  └────────────┘   │FeatureTrack│  │  obsPCL   │  │
 │                                   └────────────┘  └───────────┘  │
 └──────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
     │ SectorMapper │  │ 3D Vector    │  │ SLAM 360° Filler │
     │ → 72-bin 2D  │  │ → per-sector │  │ → rear/side bins │
     │              │  │   3D vectors │  │ → fence polygons │
     └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
            │                 │                   │
            ▼                 ▼                   ▼
    ┌──────────────────────────────────────────────────────┐
    │     OBSTACLE_DISTANCE    OBSTACLE_DISTANCE_3D        │
    │     (msg #330)           (msg #11037)                │
    │                                                      │
    │     Dynamic Fence Upload (MISSION_ITEM_INT)          │
    │             ArduCopter via pymavlink                 │
    └──────────────────────────────────────────────────────┘

ROI Grid Design:
────────────────
The SpatialLocationCalculator ROI grid is designed to simultaneously serve
both OBSTACLE_DISTANCE (needs angular bins in the horizontal plane) and
OBSTACLE_DISTANCE_3D (needs vertical layers for up/down detection).

OAK-D Lite specs: ~73° HFOV, ~58° VFOV

  Horizontal: 8 columns × ~9.125° each → maps to OBSTACLE_DISTANCE bins
  Vertical:   5 rows → provides altitude layers for 3D vectors

    ┌────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
    │ R0,C0  │ R0,C1  │ R0,C2  │ R0,C3  │ R0,C4  │ R0,C5  │ R0,C6  │ R0,C7  │ ← High above
    ├────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
    │ R1,C0  │ R1,C1  │ R1,C2  │ R1,C3  │ R1,C4  │ R1,C5  │ R1,C6  │ R1,C7  │ ← Above horizon
    ├────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
    │ R2,C0  │ R2,C1  │ R2,C2  │ R2,C3  │ R2,C4  │ R2,C5  │ R2,C6  │ R2,C7  │ ← Horizon (key row)
    ├────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
    │ R3,C0  │ R3,C1  │ R3,C2  │ R3,C3  │ R3,C4  │ R3,C5  │ R3,C6  │ R3,C7  │ ← Below horizon
    ├────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
    │ R4,C0  │ R4,C1  │ R4,C2  │ R4,C3  │ R4,C4  │ R4,C5  │ R4,C6  │ R4,C7  │ ← Ground level
    └────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘

  Total: 40 ROIs computed on VPU per frame — no host CPU cost for depth math

Coordinate Systems:
───────────────────
  OAK Camera:       X = right,   Y = down,    Z = forward  (left-handed)
  ArduPilot FRD:    X = forward, Y = right,   Z = down     (NED-like body)

  Transform: body_x = cam_z, body_y = cam_x, body_z = cam_y

Dependencies:
  pip install pymavlink numpy
  # DepthAI SDK (v3) must be installed
"""

import os
import sys
import time
import math
import threading
import logging
from typing import Optional, List, Tuple, Dict
from collections import deque
from dataclasses import dataclass, field

import numpy as np

os.environ["MAVLINK20"] = "1"
from pymavlink import mavutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
    force=True  # Override any existing handlers
)
log = logging.getLogger("SLC_Avoidance")

# Add OpenCV for visualization
try:
    import cv2
    VISUALIZATION_ENABLED = True
except ImportError:
    VISUALIZATION_ENABLED = False
    log.warning("OpenCV not available — visualization disabled")

print("Script starting...")  # Immediate output to check terminal visibility

# Start SITL in a separate terminal
log.info("Starting SITL in a new terminal...")
import subprocess
subprocess.run('start cmd /k "D:\\_agent_creation\\_drone\\run_sitl.bat"', shell=True)
log.info("SITL terminal opened.")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SLCAvoidanceConfig:
    """
    All configuration in a single dataclass.
    Tune these based on your frame, flight envelope, and OAK-D model.
    """

    # ── MAVLink ──────────────────────────────────────────────────────
    mavlink_conn: str = "tcp:127.0.0.1:5763"
    baudrate: int = 921600
    source_system: int = 1
    source_component: int = 195  # MAV_COMP_ID_PATHPLANNER

    # ── Camera / Pipeline ────────────────────────────────────────────
    camera_fps: int = 30
    camera_width: int = 640
    camera_height: int = 400
    hfov_deg: float = 73.0      # OAK-D Lite horizontal FOV
    vfov_deg: float = 58.0      # OAK-D Lite vertical FOV

    # ── SLC ROI Grid ─────────────────────────────────────────────────
    grid_cols: int = 8           # Horizontal sectors (angular bins in FOV)
    grid_rows: int = 5           # Vertical layers (for 3D avoidance)
    roi_padding: float = 0.005   # Tiny gap between ROIs to avoid overlap artifacts

    # ── Depth thresholds (millimeters) ───────────────────────────────
    depth_min_mm: int = 200      # 20cm — closer is noise
    depth_max_mm: int = 12000    # 12m — sensor max reliable range

    # ── OBSTACLE_DISTANCE (2D scan) ─────────────────────────────────
    od_num_bins: int = 72        # Fixed by MAVLink spec
    od_increment_deg: float = 5.0
    od_min_cm: int = 20
    od_max_cm: int = 1200
    od_send_hz: float = 15.0
    od_frame: int = 12           # MAV_FRAME_BODY_FRD

    # ── OBSTACLE_DISTANCE_3D ────────────────────────────────────────
    od3d_min_m: float = 0.2
    od3d_max_m: float = 12.0
    od3d_send_hz: float = 15.0
    od3d_frame: int = 12         # MAV_FRAME_BODY_FRD — mandatory

    # ── SLAM backfill for 360° coverage ─────────────────────────────
    slam_enabled: bool = True
    slam_obstacle_threshold: int = 60

    # ── Fence upload ─────────────────────────────────────────────────
    fence_update_interval_s: float = 5.0
    fence_inflation_m: float = 1.5
    fence_max_polygons: int = 5

    # ── Vertical avoidance layers ────────────────────────────────────
    # Which grid rows map to which vertical zone.
    # Row 0 = top of image (looking up), Row 4 = bottom (looking down)
    vertical_zones: Dict[str, List[int]] = field(default_factory=lambda: {
        "above":   [0, 1],       # Overhead obstacles (wires, branches)
        "horizon": [2],          # Primary flight plane (walls, trees)
        "below":   [3, 4],       # Ground/terrain obstacles
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ROI GRID GEOMETRY
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ROISector:
    """One cell in the ROI grid with its angular and pixel coordinates."""
    row: int
    col: int
    roi_index: int               # Flat index (row * cols + col)
    # Normalized image coordinates [0..1]
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    # Angular position in body frame
    h_angle_deg: float           # Horizontal angle from forward (+ = right)
    v_angle_deg: float           # Vertical angle from horizon (+ = down in FRD)
    # Corresponding OBSTACLE_DISTANCE bin (for horizon row only)
    od_bin: int = -1


class ROIGridBuilder:
    """
    Builds the SpatialLocationCalculator ROI grid and precomputes the
    mapping from each ROI cell to:
      - OBSTACLE_DISTANCE bin index (horizontal angle → bin)
      - 3D body-frame direction vector (for OBSTACLE_DISTANCE_3D)
    """

    def __init__(self, cfg: SLCAvoidanceConfig):
        self.cfg = cfg
        self.sectors: List[ROISector] = []
        self._build()

    def _build(self):
        """Pre-compute all ROI cells and their angular mappings."""
        rows = self.cfg.grid_rows
        cols = self.cfg.grid_cols
        pad = self.cfg.roi_padding
        hfov = self.cfg.hfov_deg
        vfov = self.cfg.vfov_deg

        col_width = (1.0 - 2 * pad) / cols
        row_height = (1.0 - 2 * pad) / rows

        idx = 0
        for r in range(rows):
            for c in range(cols):
                x_min = pad + c * col_width
                y_min = pad + r * row_height
                x_max = x_min + col_width
                y_max = y_min + row_height

                # Angular center of this cell
                h_center_norm = (c + 0.5) / cols           # 0..1
                h_angle = (h_center_norm - 0.5) * hfov     # -hfov/2 .. +hfov/2

                # Vertical: top row → -vfov/2 (up), bottom → +vfov/2 (down)
                v_center_norm = (r + 0.5) / rows
                v_angle = (v_center_norm - 0.5) * vfov

                # Map horizontal angle to OBSTACLE_DISTANCE bin
                od_angle = h_angle % 360
                od_bin = int(od_angle / self.cfg.od_increment_deg) % self.cfg.od_num_bins

                self.sectors.append(ROISector(
                    row=r, col=c, roi_index=idx,
                    x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max,
                    h_angle_deg=h_angle, v_angle_deg=v_angle,
                    od_bin=od_bin,
                ))
                idx += 1

        log.info(
            f"ROI grid: {rows}×{cols} = {len(self.sectors)} sectors, "
            f"covering {hfov:.0f}° H × {vfov:.0f}° V"
        )

    def get_fov_bin_range(self) -> Tuple[int, int]:
        """Which OBSTACLE_DISTANCE bins are covered by the camera FOV."""
        angles = [s.h_angle_deg for s in self.sectors]
        min_angle = min(angles) % 360
        max_angle = max(angles) % 360
        first_bin = int(min_angle / self.cfg.od_increment_deg) % self.cfg.od_num_bins
        last_bin = int(max_angle / self.cfg.od_increment_deg) % self.cfg.od_num_bins
        return first_bin, last_bin


# ═══════════════════════════════════════════════════════════════════════════════
# SLC → OBSTACLE_DISTANCE (2D Sector Mapping)
# ═══════════════════════════════════════════════════════════════════════════════

class SectorToObstacleDistance:
    """Converts SpatialLocationCalculator output into OBSTACLE_DISTANCE bins."""

    def __init__(self, grid: ROIGridBuilder, cfg: SLCAvoidanceConfig):
        self.grid = grid
        self.cfg = cfg
        self.no_obstacle = cfg.od_max_cm + 1  # Means "no obstacle in range"
        self._distances = [self.no_obstacle] * cfg.od_num_bins
        self._lock = threading.Lock()

    def update_from_slc(self, spatial_locations) -> None:
        """Process SpatialLocationCalculatorData output."""
        new_distances = [self.no_obstacle] * self.cfg.od_num_bins
        horizon_rows = set(self.cfg.vertical_zones.get("horizon", [2]))

        for i, loc in enumerate(spatial_locations):
            if i >= len(self.grid.sectors):
                break

            sector = self.grid.sectors[i]
            coords = loc.spatialCoordinates
            z_mm = coords.z    # forward distance
            x_mm = coords.x    # rightward offset

            if z_mm <= 0:
                continue  # Invalid / no depth data in this ROI

            # Horizontal distance in the ground plane
            horiz_dist_mm = math.sqrt(x_mm**2 + z_mm**2)
            horiz_dist_cm = int(horiz_dist_mm / 10.0)

            if horiz_dist_cm < self.cfg.od_min_cm or horiz_dist_cm > self.cfg.od_max_cm:
                continue

            od_bin = sector.od_bin

            # Horizon rows get priority; other rows contribute if closer
            if sector.row in horizon_rows:
                new_distances[od_bin] = min(new_distances[od_bin], horiz_dist_cm)
            else:
                new_distances[od_bin] = min(new_distances[od_bin], horiz_dist_cm)

        with self._lock:
            for i in range(self.cfg.od_num_bins):
                if new_distances[i] < self.no_obstacle:
                    self._distances[i] = new_distances[i]

    def backfill_from_slam(self, slam_distances: List[int]) -> None:
        """Fill bins outside the camera FOV with SLAM occupancy data."""
        first_bin, last_bin = self.grid.get_fov_bin_range()

        with self._lock:
            for i in range(self.cfg.od_num_bins):
                in_fov = False
                if first_bin <= last_bin:
                    in_fov = first_bin <= i <= last_bin
                else:
                    in_fov = i >= first_bin or i <= last_bin

                if not in_fov and slam_distances[i] < self.no_obstacle:
                    self._distances[i] = slam_distances[i]

    def get_distances(self) -> List[int]:
        with self._lock:
            return self._distances[:]

    def clear(self) -> None:
        with self._lock:
            self._distances = [self.no_obstacle] * self.cfg.od_num_bins


# ═══════════════════════════════════════════════════════════════════════════════
# SLC → OBSTACLE_DISTANCE_3D (Vertical-Aware 3D Vectors)
# ═══════════════════════════════════════════════════════════════════════════════

class SectorToObstacleDistance3D:
    """Converts SpatialLocationCalculator output into OBSTACLE_DISTANCE_3D."""

    def __init__(self, grid: ROIGridBuilder, cfg: SLCAvoidanceConfig):
        self.grid = grid
        self.cfg = cfg
        self._obstacles: List[Tuple[int, float, float, float]] = []
        self._lock = threading.Lock()

    def update_from_slc(self, spatial_locations) -> None:
        """Process all SLC sectors (all rows) into 3D obstacle vectors."""
        obstacles = []

        for i, loc in enumerate(spatial_locations):
            if i >= len(self.grid.sectors):
                break

            coords = loc.spatialCoordinates
            cam_x_mm = coords.x  # right
            cam_y_mm = coords.y  # down
            cam_z_mm = coords.z  # forward

            if cam_z_mm <= 0:
                continue

            # Convert to body FRD (meters)
            body_x = cam_z_mm / 1000.0   # forward
            body_y = cam_x_mm / 1000.0   # right
            body_z = cam_y_mm / 1000.0   # down

            dist_3d = math.sqrt(body_x**2 + body_y**2 + body_z**2)
            if dist_3d < self.cfg.od3d_min_m or dist_3d > self.cfg.od3d_max_m:
                continue

            sector = self.grid.sectors[i]
            obstacles.append((sector.roi_index, body_x, body_y, body_z))

        with self._lock:
            self._obstacles = obstacles

    def get_obstacles(self) -> List[Tuple[int, float, float, float]]:
        with self._lock:
            return self._obstacles[:]


# ═══════════════════════════════════════════════════════════════════════════════
# SLAM 360° BACKFILL ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class SLAMBackfillEngine:
    """Processes RTABMap SLAM outputs to provide 360° coverage."""

    def __init__(self, cfg: SLCAvoidanceConfig):
        self.cfg = cfg
        self._slam_distances = [cfg.od_max_cm + 1] * cfg.od_num_bins
        self._lock = threading.Lock()

    def update_from_occupancy_grid(self, grid_msg) -> None:
        """Ray-cast through the occupancy grid in all 72 directions."""
        try:
            grid_data = grid_msg.getFrame()
            w = grid_msg.getWidth()
            h = grid_msg.getHeight()
            res = 0.05  # 5cm resolution as set in RTABMap parameters
            grid_2d = grid_data.reshape((h, w))

            cx, cy = w // 2, h // 2
            no_obs = self.cfg.od_max_cm + 1
            new_dist = [no_obs] * self.cfg.od_num_bins
            max_steps = int(self.cfg.od_max_cm / 100.0 / res)

            for i in range(self.cfg.od_num_bins):
                angle_rad = math.radians(i * self.cfg.od_increment_deg)
                dx = math.sin(angle_rad)
                dy = -math.cos(angle_rad)

                for step in range(1, max_steps):
                    gx = int(cx + dx * step)
                    gy = int(cy + dy * step)
                    if gx < 0 or gx >= w or gy < 0 or gy >= h:
                        break
                    if grid_2d[gy, gx] > self.cfg.slam_obstacle_threshold:
                        dist_cm = int(step * res * 100)
                        new_dist[i] = max(self.cfg.od_min_cm, min(dist_cm, self.cfg.od_max_cm))
                        break

            with self._lock:
                self._slam_distances = new_dist

        except Exception as e:
            log.error(f"SLAM backfill error: {e}")

    def update_from_obstacle_pcl(self, pcl_points: np.ndarray) -> None:
        """Alternative: bin obstacle PCL points into 72 angular sectors."""
        try:
            if len(pcl_points) == 0:
                return

            x = pcl_points[:, 0]
            y = pcl_points[:, 1]
            horiz_dist = np.sqrt(x**2 + y**2)
            angles = np.degrees(np.arctan2(y, x)) % 360
            bins = (angles / self.cfg.od_increment_deg).astype(int) % self.cfg.od_num_bins

            no_obs = self.cfg.od_max_cm + 1
            new_dist = [no_obs] * self.cfg.od_num_bins

            for b in range(self.cfg.od_num_bins):
                mask = bins == b
                if np.any(mask):
                    min_d = np.min(horiz_dist[mask])
                    cm = int(min_d * 100)
                    new_dist[b] = max(self.cfg.od_min_cm, min(cm, self.cfg.od_max_cm))

            with self._lock:
                self._slam_distances = new_dist

        except Exception as e:
            log.error(f"SLAM PCL backfill error: {e}")

    def get_slam_distances(self) -> List[int]:
        with self._lock:
            return self._slam_distances[:]


# ═══════════════════════════════════════════════════════════════════════════════
# MAVLink SENDER
# ═══════════════════════════════════════════════════════════════════════════════

class MAVLinkSender:
    """Handles MAVLink connection and message transmission."""

    def __init__(self, cfg: SLCAvoidanceConfig):
        self.cfg = cfg
        self.conn = None
        self._lock = threading.Lock()
        self._running = False

    def connect(self):
        log.info(f"Connecting to {self.cfg.mavlink_conn} ...")
        self.conn = mavutil.mavlink_connection(
            self.cfg.mavlink_conn,
            baud=self.cfg.baudrate,
            source_system=self.cfg.source_system,
            source_component=self.cfg.source_component,
        )
        self.conn.wait_heartbeat(timeout=30)
        log.info(f"Connected: sys={self.conn.target_system} comp={self.conn.target_component}")

        self._running = True
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()

    def _heartbeat_loop(self):
        while self._running:
            with self._lock:
                if self.conn:
                    self.conn.mav.heartbeat_send(
                        mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                        mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0,
                    )
            time.sleep(1)

    def send_obstacle_distance(self, distances: List[int]) -> None:
        """Send OBSTACLE_DISTANCE (#330) with 72-bin radial distances."""
        with self._lock:
            self.conn.mav.obstacle_distance_send(
                int(time.monotonic() * 1e6),
                mavutil.mavlink.MAV_DISTANCE_SENSOR_LASER,
                distances,
                0,                                  # increment (ignored)
                self.cfg.od_min_cm,
                self.cfg.od_max_cm,
                self.cfg.od_increment_deg,           # increment_f
                0.0,                                 # angle_offset (0=forward)
                self.cfg.od_frame,                   # BODY_FRD
            )

    def send_obstacle_distance_3d(
        self, obstacles: List[Tuple[int, float, float, float]]
    ) -> None:
        """Send OBSTACLE_DISTANCE_3D (#11037) for each detected obstacle."""
        time_ms = int(time.monotonic() * 1000) & 0xFFFFFFFF

        with self._lock:
            for obs_id, bx, by, bz in obstacles:
                self.conn.mav.obstacle_distance_3d_send(
                    time_ms,
                    mavutil.mavlink.MAV_DISTANCE_SENSOR_LASER,
                    self.cfg.od3d_frame,             # MUST be BODY_FRD
                    obs_id & 0xFFFF,
                    float(bx), float(by), float(bz),
                    self.cfg.od3d_min_m,
                    self.cfg.od3d_max_m,
                )

    def set_params(self, params: Dict[str, float]) -> None:
        """Set ArduPilot parameters."""
        with self._lock:
            for name, val in params.items():
                self.conn.mav.param_set_send(
                    self.conn.target_system,
                    self.conn.target_component,
                    name.encode("utf-8"),
                    float(val),
                    mavutil.mavlink.MAV_PARAM_TYPE_REAL32,
                )
                time.sleep(0.05)

    def close(self):
        self._running = False
        if self.conn:
            self.conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# DepthAI v3 PIPELINE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_slc_slam_pipeline(cfg: SLCAvoidanceConfig, grid: ROIGridBuilder):
    """
    Build a DepthAI v3 pipeline with:
    1. StereoDepth → SpatialLocationCalculator (multi-ROI grid)
    2. StereoDepth → FeatureTracker → RTABMapVIO → RTABMapSLAM
    """
    try:
        import depthai as dai
    except ImportError:
        log.error("DepthAI not installed. pip install depthai")
        return None, None, None, None

    pipeline = dai.Pipeline()
    slam = None

    w, h = cfg.camera_width, cfg.camera_height

    # ── Cameras + IMU (Updated for v3) ────────────────────────────
    # In DepthAI v3, we use dai.node.Camera and specific CameraBoardSockets
    monoLeft = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    monoRight = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    
    # Request outputs specifically sized for the pipeline
    monoLeftOut = monoLeft.requestOutput((w, h))
    monoRightOut = monoRight.requestOutput((w, h))

    imu = pipeline.create(dai.node.IMU)
    imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)

    # ── Stereo Depth (Updated for v3) ─────────────────────────────
    stereo = pipeline.create(dai.node.StereoDepth)
    stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.DEFAULT)
    stereo.setLeftRightCheck(True)
    stereo.setExtendedDisparity(False)
    
    # Explicitly enable rectification so it outputs the rectified frames for the FeatureTracker
    stereo.setRectification(True)
    stereo.setRectifyEdgeFillColor(0)
    stereo.initialConfig.setLeftRightCheckThreshold(10)
    
    # Use CAM_B instead of LEFT constant
    stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)

    # Link requested outputs to stereo inputs
    monoLeftOut.link(stereo.left)
    monoRightOut.link(stereo.right)

    # ── SpatialLocationCalculator (multi-ROI grid) ────────────────
    slc = pipeline.create(dai.node.SpatialLocationCalculator)
    
    # v3 config syntax update:
    slc.inputConfig.setWaitForMessage(False)

    for sector in grid.sectors:
        roi_cfg = dai.SpatialLocationCalculatorConfigData()
        roi_cfg.depthThresholds.lowerThreshold = cfg.depth_min_mm
        roi_cfg.depthThresholds.upperThreshold = cfg.depth_max_mm
        roi_cfg.roi = dai.Rect(
            dai.Point2f(sector.x_min, sector.y_min),
            dai.Point2f(sector.x_max, sector.y_max),
        )
        try:
            roi_cfg.calculationAlgorithm = dai.SpatialLocationCalculatorAlgorithm.MIN
        except AttributeError:
            pass  # Older SDK fallback
        slc.initialConfig.addROI(roi_cfg)

    stereo.depth.link(slc.inputDepth)

    # ── Feature Tracker → RTABMap VIO → SLAM ─────────────────────
    if cfg.slam_enabled:
        try:
            ft = pipeline.create(dai.node.FeatureTracker)
            ft.setHardwareResources(1, 2)
            ft.initialConfig.setCornerDetector(
                dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS
            )
            ft.initialConfig.setNumTargetFeatures(1000)
            ft.initialConfig.setMotionEstimator(False)
            ft.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

            odom = pipeline.create(dai.node.RTABMapVIO)
            slam = pipeline.create(dai.node.RTABMapSLAM)
            slam.setParams({
                "RGBD/CreateOccupancyGrid": "true",
                "Grid/3D": "true",
                "Grid/CellSize": "0.05",  # 5cm resolution
                "Rtabmap/SaveWMState": "true",
            })

            # Pass the rectified frame to the tracker
            stereo.rectifiedLeft.link(ft.inputImage)
            ft.passthroughInputImage.link(odom.rect)
            stereo.depth.link(odom.depth)
            imu.out.link(odom.imu)
            ft.outputFeatures.link(odom.features)

            odom.transform.link(slam.odom)
            odom.passthroughRect.link(slam.rect)
            odom.passthroughDepth.link(slam.depth)

            log.info("SLAM pipeline nodes created and linked")

        except AttributeError:
            log.warning(
                "RTABMapVIO/SLAM nodes not available in this DepthAI version. "
                "SLAM backfill disabled — camera FOV only."
            )
            cfg.slam_enabled = False

    log.info(
        f"Pipeline built: {len(grid.sectors)} SLC ROIs, "
        f"SLAM={'enabled' if cfg.slam_enabled else 'disabled'}"
    )
    return pipeline, slc, slam, stereo


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class SLCAvoidanceSystem:
    """Orchestrates DepthAI pipeline with MAVLink bridging."""

    def __init__(self, cfg: SLCAvoidanceConfig = None):
        self.cfg = cfg or SLCAvoidanceConfig()
        self.grid = ROIGridBuilder(self.cfg)
        self.sector_2d = SectorToObstacleDistance(self.grid, self.cfg)
        self.sector_3d = SectorToObstacleDistance3D(self.grid, self.cfg)
        self.slam_backfill = SLAMBackfillEngine(self.cfg)
        self.mav = MAVLinkSender(self.cfg)
        self._running = False

    def start(self):
        """Full system startup."""
        self.mav.connect()
        self._configure_ardupilot()

        pipeline, slc, slam, stereo = build_slc_slam_pipeline(self.cfg, self.grid)
        if pipeline is None:
            log.warning("No DepthAI — running in test mode")
            self._run_test_mode()
            return

        self._run_pipeline(pipeline, slc, slam, stereo)

    def _configure_ardupilot(self):
        """Set all required ArduPilot parameters."""
        self.mav.set_params({
            "PRX_TYPE": 2,           # MAVLink proximity
            "AVOID_ENABLE": 7,       # All sources
            "OA_TYPE": 3,            # Dijkstra + BendyRuler combined
            "OA_BR_LOOKAHEAD": 5,    # 5m lookahead
            "OA_BR_TYPE": 2,         # Vertical BendyRuler (uses 3D data!)
            "OA_MARGIN_MAX": 2,      # 2m margin
            "FENCE_ENABLE": 1,
            "FENCE_TYPE": 4,         # Polygon
            "FENCE_ACTION": 1,       # RTL on breach
        })
        log.info("ArduPilot parameters configured")

    def _run_pipeline(self, pipeline, slc, slam, stereo):
        """Main processing loop with DepthAI hardware."""
        import depthai as dai

        self._running = True
        od_interval = 1.0 / self.cfg.od_send_hz
        od3d_interval = 1.0 / self.cfg.od3d_send_hz
        last_od = last_od3d = 0.0

        spatial_q = slc.out.createOutputQueue(maxSize=4, blocking=False)

        slam_grid_q = None
        slam_pcl_q = None
        if slam is not None:
            slam_grid_q = slam.occupancyGridMap.createOutputQueue(maxSize=2, blocking=False)
            slam_pcl_q = slam.obstaclePCL.createOutputQueue(maxSize=2, blocking=False)

        # Visualization queues
        rect_q = stereo.rectifiedLeft.createOutputQueue(maxSize=4, blocking=False)
        depth_q = stereo.depth.createOutputQueue(maxSize=4, blocking=False)

        pipeline.start()

        log.info("Pipeline running — processing SLC sectors")
        if VISUALIZATION_ENABLED:
            log.info("Visualization enabled — press 'q' to quit")

        while pipeline.isRunning() and self._running:
                now = time.time()

                # ── Read SLC data ────────────────────────────────────
                slc_data = spatial_q.tryGet()
                if slc_data is not None:
                    locations = slc_data.getSpatialLocations()
                    self.sector_2d.update_from_slc(locations)
                    self.sector_3d.update_from_slc(locations)

                # ── Read SLAM data (if available) ────────────────────
                if slam_grid_q is not None:
                    grid_data = slam_grid_q.tryGet()
                    if grid_data is not None:
                        self.slam_backfill.update_from_occupancy_grid(grid_data)
                        self.sector_2d.backfill_from_slam(
                            self.slam_backfill.get_slam_distances()
                        )
                        # Visualize occupancy grid
                        if VISUALIZATION_ENABLED:
                            grid_img = grid_data.getFrame()
                            grid_vis = cv2.normalize(grid_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                            cv2.imshow("Occupancy Grid", grid_vis)

                if slam_pcl_q is not None:
                    pcl_data = slam_pcl_q.tryGet()
                    if pcl_data is not None:
                        points = np.array(pcl_data.getPoints(), dtype=np.float32)
                        self.slam_backfill.update_from_obstacle_pcl(points)

                # ── Send OBSTACLE_DISTANCE at target rate ────────────
                if now - last_od >= od_interval:
                    self.mav.send_obstacle_distance(self.sector_2d.get_distances())
                    last_od = now

                # ── Send OBSTACLE_DISTANCE_3D at target rate ─────────
                if now - last_od3d >= od3d_interval:
                    obstacles_3d = self.sector_3d.get_obstacles()
                    if obstacles_3d:
                        self.mav.send_obstacle_distance_3d(obstacles_3d)
                    last_od3d = now

                # ── Visualization ─────────────────────────────────────
                if VISUALIZATION_ENABLED:
                    # Get rectified frame
                    rect_frame = rect_q.tryGet()
                    if rect_frame is not None:
                        rect_img = rect_frame.getCvFrame()
                        # Add status overlay
                        obstacles_2d = sum(1 for d in self.sector_2d.get_distances() if d < self.cfg.od_max_cm + 1)
                        obstacles_3d = len(self.sector_3d.get_obstacles())
                        cv2.putText(rect_img, f"2D Obstacles: {obstacles_2d}/72", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(rect_img, f"3D Obstacles: {obstacles_3d}", (10, 60), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.imshow("Rectified Left", rect_img)

                    # Get depth frame
                    depth_frame = depth_q.tryGet()
                    if depth_frame is not None:
                        depth_img = depth_frame.getFrame()
                        # Normalize depth for visualization
                        depth_vis = cv2.normalize(depth_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                        depth_colored = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
                        cv2.imshow("Depth Map", depth_colored)

                    # Check for quit key
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                time.sleep(0.001)

    def _run_test_mode(self):
        """Synthetic obstacle mode for testing without hardware."""
        self._running = True
        od_interval = 1.0 / self.cfg.od_send_hz
        od3d_interval = 1.0 / self.cfg.od3d_send_hz
        last_od = last_od3d = 0.0

        no_obs = self.cfg.od_max_cm + 1

        try:
            while self._running:
                now = time.time()

                distances = [no_obs] * self.cfg.od_num_bins
                obstacles_3d = []

                for b in list(range(0, 5)) + list(range(68, 72)):
                    distances[b] = 400

                obstacles_3d.extend([
                    (2, 3.0, 0.0, -2.0),
                    (3, 3.0, 0.5, -1.5),
                    (32, 2.0, 0.0, 1.0),
                ])

                with self.sector_2d._lock:
                    self.sector_2d._distances = distances

                with self.sector_3d._lock:
                    self.sector_3d._obstacles = obstacles_3d

                if now - last_od >= od_interval:
                    self.mav.send_obstacle_distance(self.sector_2d.get_distances())
                    last_od = now

                if now - last_od3d >= od3d_interval:
                    obs = self.sector_3d.get_obstacles()
                    if obs:
                        self.mav.send_obstacle_distance_3d(obs)
                    last_od3d = now

                time.sleep(0.01)

        except KeyboardInterrupt:
            pass
        finally:
            self._running = False
            self.mav.close()
            if VISUALIZATION_ENABLED:
                cv2.destroyAllWindows()
            log.info("Test mode stopped")

    def stop(self):
        self._running = False
        self.mav.close()
        if VISUALIZATION_ENABLED:
            cv2.destroyAllWindows()


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description="SLC + SLAM → MAVLink 3D Obstacle Avoidance"
    )
    p.add_argument("--connect", default="tcp:127.0.0.1:5763")
    p.add_argument("--test", action="store_true", help="Synthetic obstacle mode")
    p.add_argument("--cols", type=int, default=8, help="SLC grid columns (default: 8)")
    p.add_argument("--rows", type=int, default=5, help="SLC grid rows (default: 5)")
    p.add_argument("--hz", type=float, default=15, help="Send rate Hz (default: 15)")
    p.add_argument("--no-slam", action="store_true", help="Disable SLAM backfill")
    args = p.parse_args()

    cfg = SLCAvoidanceConfig(
        mavlink_conn=args.connect,
        grid_cols=args.cols,
        grid_rows=args.rows,
        od_send_hz=args.hz,
        od3d_send_hz=args.hz,
        slam_enabled=not args.no_slam,
    )

    system = SLCAvoidanceSystem(cfg)
    try:
        if args.test:
            system.mav.connect()
            system._configure_ardupilot()
            system._run_test_mode()
        else:
            system.start()
    except KeyboardInterrupt:
        system.stop()