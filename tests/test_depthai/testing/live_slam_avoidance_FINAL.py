"""
Live SLAM + Obstacle Avoidance Path Planner
============================================
- Runs OAK-D Lite with RTAB-Map SLAM continuously
- Saves/loads SLAM database for loop closure & relocalization
- Builds 3D occupancy grid from obstacle point cloud in real-time
- Continuously plans avoidance path 5m forward from current pose
- Goal is always 5m ahead in the camera's forward direction (body frame)
  so an LLM can later override the goal with a new body-relative position

Usage:
    python live_slam_avoidance.py                  # Fresh SLAM session
    python live_slam_avoidance.py --load            # Resume from saved DB (relocalize)
    python live_slam_avoidance.py --db path/to.db   # Use specific DB file
"""

import time
import math
import argparse
import numpy as np
from pathlib import Path
from heapq import heappush, heappop
from collections import deque

import depthai as dai


# =============================================================================
# Occupancy Grid (lightweight, continuously updated)
# =============================================================================
class LiveOccupancyGrid:
    """Rolling 3D occupancy grid updated from SLAM obstacle point clouds."""

    def __init__(self, cell_size=0.10, half_extent=8.0, z_min=-1.0, z_max=4.0):
        self.cell_size = cell_size
        self.half_extent = half_extent
        self.z_min = z_min
        self.z_max = z_max

        # Grid dimensions
        side = int(2 * half_extent / cell_size)
        z_cells = int((z_max - z_min) / cell_size)
        self.nx, self.ny, self.nz = side, side, z_cells

        # 0 = free, >0 = obstacle hit count
        self.grid = np.zeros((self.nx, self.ny, self.nz), dtype=np.int16)
        self.obstacle_thresh = 1  # hits needed to mark occupied

        # Origin in world frame (grid centre tracks the drone loosely)
        self.origin_x = 0.0
        self.origin_y = 0.0

    # -- coordinate helpers ---------------------------------------------------
    def _w2g(self, x, y, z):
        gx = int((x - self.origin_x + self.half_extent) / self.cell_size)
        gy = int((y - self.origin_y + self.half_extent) / self.cell_size)
        gz = int((z - self.z_min) / self.cell_size)
        return gx, gy, gz

    def _g2w(self, gx, gy, gz):
        x = gx * self.cell_size + self.origin_x - self.half_extent
        y = gy * self.cell_size + self.origin_y - self.half_extent
        z = gz * self.cell_size + self.z_min
        return x, y, z

    def _in_bounds(self, gx, gy, gz):
        return 0 <= gx < self.nx and 0 <= gy < self.ny and 0 <= gz < self.nz

    def is_free(self, gx, gy, gz):
        if not self._in_bounds(gx, gy, gz):
            return False
        return self.grid[gx, gy, gz] < self.obstacle_thresh

    # -- update from point cloud data -----------------------------------------
    def insert_obstacle_points(self, points, inflate_cells=2):
        """Insert obstacle points (Nx3 numpy array) into grid with inflation."""
        for pt in points:
            cx, cy, cz = self._w2g(pt[0], pt[1], pt[2])
            for dx in range(-inflate_cells, inflate_cells + 1):
                for dy in range(-inflate_cells, inflate_cells + 1):
                    for dz in range(-inflate_cells, inflate_cells + 1):
                        nx, ny, nz = cx + dx, cy + dy, cz + dz
                        if self._in_bounds(nx, ny, nz):
                            self.grid[nx, ny, nz] += 1

    def mark_free_along_ray(self, origin, point, step=None):
        """Clear cells along a ray from origin to point (ray-casting free space)."""
        if step is None:
            step = self.cell_size
        direction = np.array(point) - np.array(origin)
        dist = np.linalg.norm(direction)
        if dist < 1e-6:
            return
        direction /= dist
        t = 0.0
        while t < dist - step:
            p = np.array(origin) + direction * t
            gx, gy, gz = self._w2g(p[0], p[1], p[2])
            if self._in_bounds(gx, gy, gz):
                self.grid[gx, gy, gz] = max(0, self.grid[gx, gy, gz] - 1)
            t += step

    def decay(self, amount=1):
        """Slowly decay obstacle counts so stale obstacles fade."""
        mask = self.grid > 0
        self.grid[mask] = np.maximum(0, self.grid[mask] - amount)

    def occupied_count(self):
        return int(np.sum(self.grid >= self.obstacle_thresh))


# =============================================================================
# A* 3D path planner (same logic as path_planner_3d.py, simplified)
# =============================================================================
class FastPlanner3D:
    """Lightweight A* on the live occupancy grid."""

    def __init__(self, grid: LiveOccupancyGrid):
        self.g = grid

    def plan(self, start_world, goal_world, max_nodes=50000):
        """Return list of (x,y,z) world waypoints or None."""
        sg = self.g._w2g(*start_world)
        gg = self.g._w2g(*goal_world)

        # Clamp to bounds
        sg = tuple(max(0, min(sg[i], [self.g.nx, self.g.ny, self.g.nz][i] - 1)) for i in range(3))
        gg = tuple(max(0, min(gg[i], [self.g.nx, self.g.ny, self.g.nz][i] - 1)) for i in range(3))

        if not self.g.is_free(*sg):
            # Try to nudge start into free space
            sg = self._nudge_free(sg)
            if sg is None:
                return None
        if not self.g.is_free(*gg):
            gg = self._nudge_free(gg)
            if gg is None:
                return None

        open_set = [(0.0, sg)]
        came_from = {}
        g_score = {sg: 0.0}
        explored = 0

        while open_set and explored < max_nodes:
            _, cur = heappop(open_set)
            explored += 1
            if cur == gg:
                return self._reconstruct(came_from, sg, gg)

            for nb, cost in self._neighbors(cur):
                tg = g_score[cur] + cost
                if nb not in g_score or tg < g_score[nb]:
                    came_from[nb] = cur
                    g_score[nb] = tg
                    f = tg + self._h(nb, gg)
                    heappush(open_set, (f, nb))

        return None  # no path

    def _neighbors(self, pos):
        out = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    nb = (pos[0] + dx, pos[1] + dy, pos[2] + dz)
                    if self.g.is_free(*nb):
                        out.append((nb, math.sqrt(dx * dx + dy * dy + dz * dz)))
        return out

    @staticmethod
    def _h(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

    def _nudge_free(self, pos, radius=5):
        for r in range(1, radius + 1):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    for dz in range(-r, r + 1):
                        nb = (pos[0] + dx, pos[1] + dy, pos[2] + dz)
                        if self.g.is_free(*nb):
                            return nb
        return None

    def _reconstruct(self, came_from, start, goal):
        path = []
        cur = goal
        while cur != start:
            path.append(self.g._g2w(*cur))
            cur = came_from[cur]
        path.append(self.g._g2w(*start))
        path.reverse()
        return path

    @staticmethod
    def smooth(path, iterations=8, alpha=0.45):
        if path is None or len(path) < 3:
            return path
        pts = np.array(path, dtype=float)
        for _ in range(iterations):
            for i in range(1, len(pts) - 1):
                pts[i] = (1 - alpha) * pts[i] + alpha * 0.5 * (pts[i - 1] + pts[i + 1])
        return pts.tolist()

    @staticmethod
    def downsample(path, max_wps=20):
        if path is None or len(path) <= max_wps:
            return path
        step = max(1, len(path) // max_wps)
        out = [path[0]]
        for i in range(step, len(path) - 1, step):
            out.append(path[i])
        out.append(path[-1])
        return out


# =============================================================================
# Quaternion -> forward direction helper
# =============================================================================
def quat_forward(qw, qx, qy, qz):
    """Return unit forward vector (camera Z axis) from quaternion."""
    # Rotate [0, 0, 1] by quaternion
    fx = 2.0 * (qx * qz + qw * qy)
    fy = 2.0 * (qy * qz - qw * qx)
    fz = 1.0 - 2.0 * (qx * qx + qy * qy)
    norm = math.sqrt(fx * fx + fy * fy + fz * fz)
    if norm < 1e-9:
        return (1.0, 0.0, 0.0)
    return (fx / norm, fy / norm, fz / norm)


# =============================================================================
# Point cloud parsing helper
# =============================================================================
def pcl_to_numpy(pcl_data):
    """Convert DepthAI PointCloudData to Nx3 numpy array."""
    points = pcl_data.getPoints()
    if len(points) == 0:
        return np.empty((0, 3))
    arr = np.array(points, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 3)
    return arr


# =============================================================================
# Main pipeline
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="Live SLAM + Avoidance")
    parser.add_argument("--load", action="store_true",
                        help="Load existing SLAM database for relocalization")
    parser.add_argument("--db", type=str, default="slam_data/rtabmap_live.db",
                        help="Path to SLAM database file")
    parser.add_argument("--goal-dist", type=float, default=5.0,
                        help="Goal distance ahead in meters (default 5)")
    parser.add_argument("--replan-hz", type=float, default=2.0,
                        help="Path re-planning rate in Hz (default 2)")
    parser.add_argument("--cell-size", type=float, default=0.10,
                        help="Occupancy grid cell size in metres (default 0.10)")
    args = parser.parse_args()

    db_path = str(Path(args.db).resolve())
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # -- RTAB-Map parameters optimized for loop closure + relocalization -------
    slam_params = {
        # Core
        "Rtabmap/DetectionRate": "2.0",
        "Rtabmap/TimeThr": "0",
        "Rtabmap/MemoryThr": "300",
        "Rtabmap/LoopThr": "0.11",
        "Rtabmap/SaveWMState": "true",

        # RGBD
        "RGBD/Enabled": "true",
        "RGBD/LinearUpdate": "0.1",
        "RGBD/AngularUpdate": "0.1",
        "RGBD/CreateOccupancyGrid": "true",
        "RGBD/ProximityBySpace": "true",
        "RGBD/LocalRadius": "10.0",
        "RGBD/MaxLoopClosureDistance": "15.0",

        # Visual features
        "Vis/MaxFeatures": "800",
        "Vis/MinInliers": "15",
        "Vis/InlierDistance": "0.1",

        # Grid (3D obstacle cloud)
        "Grid/3D": "true",
        "Grid/CellSize": "0.05",
        "Grid/RangeMax": "8.0",
        "Grid/FromDepth": "true",
        "Grid/GroundIsObstacle": "false",

        # Keypoint detector
        "Kp/MaxFeatures": "800",
        "Kp/DetectorStrategy": "8",

        # Optimizer
        "Optimizer/Strategy": "1",
        "Optimizer/Iterations": "20",

        # Memory
        "Mem/IncrementalMemory": "true",
        "Mem/ImageKept": "true",       # Keep images for relocalization
        "Mem/STMSize": "30",
    }

    # -- Build DepthAI pipeline ------------------------------------------------
    with dai.Pipeline() as p:
        fps = 30
        width, height = 640, 400

        # Camera nodes
        left = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=fps)
        right = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=fps)
        imu = p.create(dai.node.IMU)
        stereo = p.create(dai.node.StereoDepth)
        featureTracker = p.create(dai.node.FeatureTracker)
        odom = p.create(dai.node.RTABMapVIO)
        slam = p.create(dai.node.RTABMapSLAM)

        # SLAM config
        slam.setParams(slam_params)
        slam.setDatabasePath(db_path)
        slam.setSaveDatabaseOnClose(True)          # Always persist the map
        slam.setSaveDatabasePeriodically(True)
        slam.setSaveDatabasePeriod(30.0)           # Auto-save every 30s
        if args.load:
            slam.setLoadDatabaseOnStart(True)      # Relocalize into existing map
            print(f"[SLAM] Will load existing DB: {db_path}")
        else:
            print(f"[SLAM] Fresh session, DB will be saved to: {db_path}")

        # IMU
        imu.enableIMUSensor(
            [dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
        imu.setBatchReportThreshold(1)
        imu.setMaxBatchReports(10)

        # Feature tracker
        featureTracker.setHardwareResources(1, 2)
        featureTracker.initialConfig.setCornerDetector(
            dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS)
        featureTracker.initialConfig.setNumTargetFeatures(1000)
        featureTracker.initialConfig.setMotionEstimator(False)
        featureTracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

        # Stereo depth
        stereo.setExtendedDisparity(False)
        stereo.setLeftRightCheck(True)
        stereo.setRectifyEdgeFillColor(0)
        stereo.enableDistortionCorrection(True)
        stereo.initialConfig.setLeftRightCheckThreshold(10)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)

        # Linking
        left.requestOutput((width, height)).link(stereo.left)
        right.requestOutput((width, height)).link(stereo.right)
        stereo.rectifiedLeft.link(featureTracker.inputImage)
        featureTracker.passthroughInputImage.link(odom.rect)
        stereo.depth.link(odom.depth)
        imu.out.link(odom.imu)
        featureTracker.outputFeatures.link(odom.features)

        odom.transform.link(slam.odom)
        odom.passthroughRect.link(slam.rect)
        odom.passthroughDepth.link(slam.depth)

        # Output queues
        q_transform = slam.transform.createOutputQueue(maxSize=1, blocking=False)
        q_obstacle = slam.obstaclePCL.createOutputQueue(maxSize=1, blocking=False)

        # -- Avoidance components ----------------------------------------------
        occ_grid = LiveOccupancyGrid(cell_size=args.cell_size)
        planner = FastPlanner3D(occ_grid)
        replan_interval = 1.0 / args.replan_hz
        last_replan_time = 0.0

        # Current state
        cur_x = cur_y = cur_z = 0.0
        cur_qw, cur_qx, cur_qy, cur_qz = 1.0, 0.0, 0.0, 0.0
        current_path = None
        pose_count = 0
        decay_counter = 0

        # -- Start pipeline ----------------------------------------------------
        p.start()

        print("=" * 70)
        print("Live SLAM + Obstacle Avoidance")
        print(f"  DB path       : {db_path}")
        print(f"  Goal distance : {args.goal_dist}m forward from body")
        print(f"  Replan rate   : {args.replan_hz} Hz")
        print(f"  Grid cell     : {args.cell_size}m")
        print("  Press Ctrl+C to stop (DB auto-saved on exit)")
        print("=" * 70)

        try:
            while p.isRunning():
                now = time.monotonic()

                # ---- 1. Read SLAM pose ----
                if q_transform.has():
                    tf = q_transform.get()
                    t = tf.getTranslation()
                    q = tf.getQuaternion()
                    cur_x, cur_y, cur_z = t.x, t.y, t.z
                    cur_qw, cur_qx, cur_qy, cur_qz = q.qw, q.qx, q.qy, q.qz
                    pose_count += 1

                    if pose_count % 10 == 0:
                        print(f"[POSE #{pose_count:>5}]  "
                              f"x={cur_x:+.3f}  y={cur_y:+.3f}  z={cur_z:+.3f}  "
                              f"obs_cells={occ_grid.occupied_count()}")

                # ---- 2. Read obstacle point cloud & update grid ----
                if q_obstacle.has():
                    pcl_msg = q_obstacle.get()
                    pts = pcl_to_numpy(pcl_msg)
                    if pts.shape[0] > 0:
                        # Subsample if too many points
                        if pts.shape[0] > 5000:
                            idx = np.random.choice(pts.shape[0], 5000, replace=False)
                            pts = pts[idx]
                        occ_grid.insert_obstacle_points(pts, inflate_cells=2)

                    # Periodic decay so stale obstacles fade
                    decay_counter += 1
                    if decay_counter >= 10:
                        occ_grid.decay(amount=1)
                        decay_counter = 0

                # ---- 3. Re-plan path at fixed rate ----
                if now - last_replan_time >= replan_interval and pose_count > 0:
                    last_replan_time = now

                    # Goal = 5m forward from current pose in body frame
                    fwd = quat_forward(cur_qw, cur_qx, cur_qy, cur_qz)
                    goal_x = cur_x + fwd[0] * args.goal_dist
                    goal_y = cur_y + fwd[1] * args.goal_dist
                    goal_z = cur_z + fwd[2] * args.goal_dist

                    start = (cur_x, cur_y, cur_z)
                    goal = (goal_x, goal_y, goal_z)

                    raw_path = planner.plan(start, goal)
                    if raw_path is not None:
                        smoothed = FastPlanner3D.smooth(raw_path)
                        current_path = FastPlanner3D.downsample(smoothed, max_wps=20)
                        print(f"  [PATH] {len(current_path)} waypoints  "
                              f"start=({start[0]:+.2f},{start[1]:+.2f},{start[2]:+.2f})  "
                              f"goal=({goal[0]:+.2f},{goal[1]:+.2f},{goal[2]:+.2f})")
                    else:
                        current_path = None
                        print(f"  [PATH] No path found to "
                              f"({goal_x:+.2f},{goal_y:+.2f},{goal_z:+.2f})")

                time.sleep(0.005)

        except KeyboardInterrupt:
            print("\n\n[STOP] Ctrl+C received. SLAM database saving on exit...")

    # Pipeline context manager closes pipeline, SLAM saves DB automatically
    print(f"[DONE] DB saved to: {db_path}")
    print(f"       Total poses: {pose_count}")
    if current_path:
        print(f"       Last path had {len(current_path)} waypoints")


if __name__ == "__main__":
    main()
