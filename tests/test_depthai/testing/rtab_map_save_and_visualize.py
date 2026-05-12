"""
RTAB-Map SLAM State Saving and Visualization
=============================================
Save SLAM map data, occupancy grids, and trajectory for offline visualization
and path planning
"""

import time
import depthai as dai
import numpy as np
import pickle
import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SLAMStateManager:
    """Manages saving and loading of SLAM state data"""

    def __init__(self, save_dir="slam_data"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

        # Data storage
        self.trajectory = []
        self.timestamps = []
        self.map_data = {
            'nodes': [],
            'edges': [],
            'loop_closures': []
        }
        self.occupancy_grid = None
        self.point_cloud = []

    def add_pose(self, timestamp, x, y, z, qw, qx, qy, qz):
        """Add a pose to the trajectory"""
        self.trajectory.append({
            'timestamp': str(timestamp),
            'position': {'x': float(x), 'y': float(y), 'z': float(z)},
            'orientation': {'qw': float(qw), 'qx': float(qx), 'qy': float(qy), 'qz': float(qz)}
        })
        self.timestamps.append(timestamp)

    def save_trajectory(self, filename=None):
        """Save trajectory to JSON file"""
        if filename is None:
            filename = f"trajectory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = self.save_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.trajectory, f, indent=2)

        print(f"Trajectory saved to: {filepath}")
        return filepath

    def save_trajectory_numpy(self, filename=None):
        """Save trajectory as numpy array for fast loading"""
        if filename is None:
            filename = f"trajectory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy"

        # Convert to numpy array: [timestamp, x, y, z, qw, qx, qy, qz]
        traj_array = np.array([
            [i,
             t['position']['x'], t['position']['y'], t['position']['z'],
             t['orientation']['qw'], t['orientation']['qx'],
             t['orientation']['qy'], t['orientation']['qz']]
            for i, t in enumerate(self.trajectory)
        ])

        filepath = self.save_dir / filename
        np.save(filepath, traj_array)

        print(f"Trajectory (numpy) saved to: {filepath}")
        return filepath

    def save_point_cloud(self, points, filename=None):
        """Save point cloud data"""
        if filename is None:
            filename = f"pointcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy"

        filepath = self.save_dir / filename
        np.save(filepath, np.array(points))

        print(f"Point cloud saved to: {filepath}")
        return filepath

    def save_occupancy_grid(self, grid_data, filename=None):
        """Save occupancy grid"""
        if filename is None:
            filename = f"occupancy_grid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy"

        filepath = self.save_dir / filename
        np.save(filepath, grid_data)

        print(f"Occupancy grid saved to: {filepath}")
        return filepath

    def save_full_state(self, prefix="slam_state"):
        """Save complete SLAM state"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save all components
        traj_file = self.save_trajectory(f"{prefix}_trajectory_{timestamp}.json")
        traj_numpy = self.save_trajectory_numpy(f"{prefix}_trajectory_{timestamp}.npy")

        # Save metadata
        metadata = {
            'timestamp': timestamp,
            'num_poses': len(self.trajectory),
            'duration': str(self.timestamps[-1] - self.timestamps[0]) if len(self.timestamps) > 1 else "0",
            'trajectory_file': str(traj_file.name),
            'trajectory_numpy': str(traj_numpy.name),
        }

        metadata_file = self.save_dir / f"{prefix}_metadata_{timestamp}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"\nFull SLAM state saved with prefix: {prefix}_{timestamp}")
        return metadata_file

    def load_trajectory(self, filepath):
        """Load trajectory from file"""
        with open(filepath, 'r') as f:
            self.trajectory = json.load(f)
        print(f"Loaded {len(self.trajectory)} poses from {filepath}")
        return self.trajectory

    def load_trajectory_numpy(self, filepath):
        """Load trajectory from numpy file"""
        data = np.load(filepath)
        print(f"Loaded {len(data)} poses from {filepath}")
        return data


class PathPlanner:
    """A* path planner using occupancy grid"""

    def __init__(self, occupancy_grid, cell_size=0.05, origin=(0, 0)):
        """
        Initialize path planner

        Args:
            occupancy_grid: 2D numpy array (1=occupied, 0=free, -1=unknown)
            cell_size: Size of each grid cell in meters
            origin: (x, y) coordinates of grid origin
        """
        self.grid = occupancy_grid
        self.cell_size = cell_size
        self.origin = origin
        self.height, self.width = occupancy_grid.shape

    def world_to_grid(self, x, y):
        """Convert world coordinates to grid coordinates"""
        grid_x = int((x - self.origin[0]) / self.cell_size)
        grid_y = int((y - self.origin[1]) / self.cell_size)
        return grid_x, grid_y

    def grid_to_world(self, grid_x, grid_y):
        """Convert grid coordinates to world coordinates"""
        x = grid_x * self.cell_size + self.origin[0]
        y = grid_y * self.cell_size + self.origin[1]
        return x, y

    def is_valid(self, x, y):
        """Check if grid cell is valid and free"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y, x] == 0  # Free space

    def get_neighbors(self, x, y):
        """Get valid neighboring cells (8-connected)"""
        neighbors = []
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                # Diagonal cost is sqrt(2), straight is 1
                cost = 1.414 if dx != 0 and dy != 0 else 1.0
                neighbors.append((nx, ny, cost))
        return neighbors

    def heuristic(self, a, b):
        """Euclidean distance heuristic"""
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def plan_path(self, start_world, goal_world, inflation_radius=0):
        """
        Plan path from start to goal using A* algorithm

        Args:
            start_world: (x, y) start position in world coordinates
            goal_world: (x, y) goal position in world coordinates
            inflation_radius: Number of cells to inflate obstacles

        Returns:
            List of (x, y) waypoints in world coordinates, or None if no path found
        """
        # Convert to grid coordinates
        start = self.world_to_grid(*start_world)
        goal = self.world_to_grid(*goal_world)

        # Validate start and goal
        if not self.is_valid(*start):
            print(f"Start position {start_world} is not valid!")
            return None
        if not self.is_valid(*goal):
            print(f"Goal position {goal_world} is not valid!")
            return None

        # A* implementation
        from heapq import heappush, heappop

        open_set = []
        heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = heappop(open_set)[1]

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()

                # Convert to world coordinates
                world_path = [self.grid_to_world(x, y) for x, y in path]
                return world_path

            for neighbor_x, neighbor_y, cost in self.get_neighbors(*current):
                neighbor = (neighbor_x, neighbor_y)
                tentative_g_score = g_score[current] + cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

        print("No path found!")
        return None

    def smooth_path(self, path, iterations=5):
        """Smooth path using simple averaging"""
        if path is None or len(path) < 3:
            return path

        smoothed = np.array(path)
        for _ in range(iterations):
            for i in range(1, len(smoothed) - 1):
                smoothed[i] = 0.5 * smoothed[i] + 0.25 * (smoothed[i-1] + smoothed[i+1])

        return smoothed.tolist()


def visualize_slam_data(trajectory_file, save_plot=True):
    """Visualize saved SLAM trajectory"""

    manager = SLAMStateManager()
    trajectory = manager.load_trajectory(trajectory_file)

    # Extract positions
    x = [p['position']['x'] for p in trajectory]
    y = [p['position']['y'] for p in trajectory]
    z = [p['position']['z'] for p in trajectory]

    # Create 3D plot
    fig = plt.figure(figsize=(15, 10))

    # 3D trajectory
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.plot(x, y, z, 'b-', linewidth=1, alpha=0.6)
    ax1.scatter([x[0]], [y[0]], [z[0]], c='g', marker='o', s=100, label='Start')
    ax1.scatter([x[-1]], [y[-1]], [z[-1]], c='r', marker='o', s=100, label='End')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('3D Trajectory')
    ax1.legend()
    ax1.grid(True)

    # Top view (X-Y)
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(x, y, 'b-', linewidth=1, alpha=0.6)
    ax2.scatter([x[0]], [y[0]], c='g', marker='o', s=100, label='Start')
    ax2.scatter([x[-1]], [y[-1]], c='r', marker='o', s=100, label='End')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_title('Top View (X-Y)')
    ax2.legend()
    ax2.grid(True)
    ax2.axis('equal')

    # Side view (X-Z)
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(x, z, 'b-', linewidth=1, alpha=0.6)
    ax3.scatter([x[0]], [z[0]], c='g', marker='o', s=100, label='Start')
    ax3.scatter([x[-1]], [z[-1]], c='r', marker='o', s=100, label='End')
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Z (m)')
    ax3.set_title('Side View (X-Z)')
    ax3.legend()
    ax3.grid(True)

    # Front view (Y-Z)
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(y, z, 'b-', linewidth=1, alpha=0.6)
    ax4.scatter([y[0]], [z[0]], c='g', marker='o', s=100, label='Start')
    ax4.scatter([y[-1]], [z[-1]], c='r', marker='o', s=100, label='End')
    ax4.set_xlabel('Y (m)')
    ax4.set_ylabel('Z (m)')
    ax4.set_title('Front View (Y-Z)')
    ax4.legend()
    ax4.grid(True)

    plt.tight_layout()

    if save_plot:
        plot_file = Path(trajectory_file).parent / f"trajectory_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {plot_file}")

    plt.show()


def main_slam_with_saving():
    """Main SLAM pipeline with state saving"""

    # Initialize state manager
    state_manager = SLAMStateManager(save_dir="slam_data")

    # RTAB-Map parameters optimized for mapping
    params = {
        "Rtabmap/DetectionRate": "2.0",
        "Rtabmap/TimeThr": "0",
        "Rtabmap/MemoryThr": "300",
        "Rtabmap/LoopThr": "0.11",
        "Rtabmap/SaveWMState": "true",

        "RGBD/Enabled": "true",
        "RGBD/LinearUpdate": "0.1",
        "RGBD/AngularUpdate": "0.1",
        "RGBD/CreateOccupancyGrid": "true",
        "RGBD/ProximityBySpace": "true",
        "RGBD/LocalRadius": "10.0",

        "Vis/MaxFeatures": "800",
        "Vis/MinInliers": "15",
        "Vis/InlierDistance": "0.1",

        "Grid/3D": "true",
        "Grid/CellSize": "0.05",
        "Grid/RangeMax": "10.0",
        "Grid/FromDepth": "true",
        "Grid/GroundIsObstacle": "false",

        "Kp/MaxFeatures": "800",
        "Kp/DetectorStrategy": "8",

        "Mem/IncrementalMemory": "true",
        "Mem/ImageKept": "false",  # Set to true if you want to save images
    }

    with dai.Pipeline() as p:
        fps = 30
        width = 640
        height = 400

        # Define sources
        left = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=fps)
        right = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=fps)
        imu = p.create(dai.node.IMU)
        stereo = p.create(dai.node.StereoDepth)
        featureTracker = p.create(dai.node.FeatureTracker)
        odom = p.create(dai.node.RTABMapVIO)
        slam = p.create(dai.node.RTABMapSLAM)

        # Apply parameters
        slam.setParams(params)

        # Configure nodes
        imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
        imu.setBatchReportThreshold(1)
        imu.setMaxBatchReports(10)

        featureTracker.setHardwareResources(1, 2)
        featureTracker.initialConfig.setCornerDetector(dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS)
        featureTracker.initialConfig.setNumTargetFeatures(1000)
        featureTracker.initialConfig.setMotionEstimator(False)
        featureTracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

        stereo.setExtendedDisparity(False)
        stereo.setLeftRightCheck(True)
        stereo.setRectifyEdgeFillColor(0)
        stereo.enableDistortionCorrection(True)
        stereo.initialConfig.setLeftRightCheckThreshold(10)
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)

        # Linking
        left.requestOutput((width, height)).link(stereo.left)
        right.requestOutput((width, height)).link(stereo.right)
        featureTracker.passthroughInputImage.link(odom.rect)
        stereo.rectifiedLeft.link(featureTracker.inputImage)
        stereo.depth.link(odom.depth)
        imu.out.link(odom.imu)
        featureTracker.outputFeatures.link(odom.features)

        odom.transform.link(slam.odom)
        odom.passthroughRect.link(slam.rect)
        odom.passthroughDepth.link(slam.depth)

        # Create output queue
        slamTransformQueue = slam.transform.createOutputQueue(maxSize=1, blocking=False)

        # Setup visualization
        plt.ion()
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        trajectory_x = []
        trajectory_y = []
        trajectory_z = []

        p.start()

        print("\n" + "="*80)
        print("RTAB-Map SLAM with State Saving")
        print("="*80)
        print("Controls:")
        print("  - Press Ctrl+C to stop and save SLAM state")
        print("  - Data will be saved to 'slam_data' directory")
        print("="*80)
        print(f"{'Timestamp':<25} {'X':<10} {'Y':<10} {'Z':<10} {'Poses':<8}")
        print("-"*80)

        frame_count = 0
        save_interval = 100  # Auto-save every 100 frames

        try:
            while p.isRunning():
                if slamTransformQueue.has():
                    transform = slamTransformQueue.get()
                    timestamp = dai.Clock.now()

                    # Get pose
                    translation = transform.getTranslation()
                    x, y, z = translation.x, translation.y, translation.z

                    quaternion = transform.getQuaternion()
                    qw, qx, qy, qz = quaternion.qw, quaternion.qx, quaternion.qy, quaternion.qz

                    # Save to state manager
                    state_manager.add_pose(timestamp, x, y, z, qw, qx, qy, qz)

                    # Store for visualization
                    trajectory_x.append(x)
                    trajectory_y.append(y)
                    trajectory_z.append(z)

                    # Print progress
                    print(f"{timestamp!s:<25} {x:<10.4f} {y:<10.4f} {z:<10.4f} {len(trajectory_x):<8}")

                    # Update visualization every 5 frames
                    frame_count += 1
                    if frame_count % 5 == 0:
                        ax.clear()
                        ax.set_xlabel('X (m)')
                        ax.set_ylabel('Y (m)')
                        ax.set_zlabel('Z (m)')
                        ax.set_title(f'RTAB-Map SLAM - {len(trajectory_x)} poses')

                        if len(trajectory_x) > 0:
                            ax.plot(trajectory_x, trajectory_y, trajectory_z, 'b-', linewidth=1, alpha=0.6)
                            ax.scatter([x], [y], [z], c='r', marker='o', s=100, label='Current')
                            if len(trajectory_x) > 1:
                                ax.scatter([trajectory_x[0]], [trajectory_y[0]], [trajectory_z[0]],
                                         c='g', marker='o', s=100, label='Start')
                            ax.legend()
                            ax.grid(True)

                        plt.draw()
                        plt.pause(0.001)

                    # Auto-save periodically
                    if frame_count % save_interval == 0:
                        print(f"\n[Auto-save] Saving state at {len(trajectory_x)} poses...")
                        state_manager.save_full_state(prefix="autosave")
                        print(f"[Auto-save] Complete!\n")

                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\n\nStopping SLAM and saving final state...")

        # Final save
        print("\n" + "="*80)
        print("Saving final SLAM state...")
        metadata_file = state_manager.save_full_state(prefix="final")
        print(f"SLAM state saved successfully!")
        print(f"Metadata: {metadata_file}")
        print(f"Total poses collected: {len(state_manager.trajectory)}")
        print("="*80)

        plt.ioff()
        plt.show()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "visualize":
        # Visualize mode
        if len(sys.argv) > 2:
            visualize_slam_data(sys.argv[2])
        else:
            print("Usage: python rtab_map_save_and_visualize.py visualize <trajectory_file.json>")
    else:
        # Run SLAM with saving
        main_slam_with_saving()
