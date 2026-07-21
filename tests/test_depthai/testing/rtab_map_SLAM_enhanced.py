"""
Enhanced RTAB-Map SLAM with Advanced Parameter Configuration
==============================================================
Based on rtab_map_SLAM-60fps.py with expanded parameter options
"""

import time
import depthai as dai
import matplotlib.pyplot as plt

# ===========================
# PARAMETER CONFIGURATIONS
# ===========================
# Choose one of the configurations below or create your own!

# CONFIGURATION 1: High Performance (Recommended for drones)
params_high_performance = {
    # Core SLAM Settings
    "Rtabmap/DetectionRate": "3.0",              # 3 Hz detection rate for fast movement
    "Rtabmap/TimeThr": "0",                      # No time limit for map updates
    "Rtabmap/MemoryThr": "200",                  # Max 200 nodes in working memory
    "Rtabmap/LoopThr": "0.11",                   # Loop closure threshold

    # RGBD Configuration
    "RGBD/Enabled": "true",                      # Enable RGB-D SLAM
    "RGBD/LinearUpdate": "0.1",                  # Update every 10cm movement
    "RGBD/AngularUpdate": "0.1",                 # Update every ~6 degree rotation
    "RGBD/OptimizeFromGraphEnd": "false",        # Optimize from start
    "RGBD/CreateOccupancyGrid": "true",          # Create occupancy grid
    "RGBD/LocalRadius": "10.0",                  # 10m local map radius
    "RGBD/MaxLoopClosureDistance": "10.0",       # Allow loop closures up to 10m

    # Visual Features
    "Vis/MaxFeatures": "800",                    # Extract up to 800 features
    "Vis/MinInliers": "15",                      # Minimum 15 inliers for valid transform
    "Vis/InlierDistance": "0.1",                 # Max 10cm inlier distance
    "Vis/EstimationType": "0",                   # 0=3D-3D matching

    # Keypoint Detection
    "Kp/MaxFeatures": "800",                     # Max keypoints to extract
    "Kp/DetectorStrategy": "8",                  # 8=ORB (fast and robust)

    # Grid Settings
    "Grid/3D": "true",                           # Enable 3D grid
    "Grid/CellSize": "0.05",                     # 5cm grid cells
    "Grid/RangeMax": "5.0",                      # 5m max range
    "Grid/ClusterRadius": "0.1",                 # 10cm cluster radius
    "Grid/GroundIsObstacle": "false",            # Don't mark ground as obstacle

    # Optimizer
    "Optimizer/Strategy": "1",                   # Use g2o optimizer
    "Optimizer/Iterations": "20",                # 20 iterations

    # Memory & Database
    "Rtabmap/SaveWMState": "true",               # Save working memory
    "Mem/IncrementalMemory": "true",             # SLAM mode (not localization)
}

# CONFIGURATION 2: Maximum Accuracy (Slower, more detailed)
params_max_accuracy = {
    "Rtabmap/DetectionRate": "1.0",
    "Rtabmap/MemoryThr": "0",                    # Unlimited memory
    "Rtabmap/TimeThr": "700",
    "Rtabmap/LoopThr": "0.15",

    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.05",                 # Very frequent updates
    "RGBD/AngularUpdate": "0.05",
    "RGBD/CreateOccupancyGrid": "true",
    "RGBD/OptimizeMaxError": "3.0",
    "RGBD/LocalRadius": "15.0",
    "RGBD/NeighborLinkRefining": "true",
    "RGBD/ProximityBySpace": "true",

    "Vis/MaxFeatures": "1000",
    "Vis/MinInliers": "20",
    "Vis/InlierDistance": "0.05",

    "Kp/MaxFeatures": "1000",
    "Kp/DetectorStrategy": "6",                  # GFTT detector

    "GFTT/QualityLevel": "0.001",
    "GFTT/MinDistance": "7.0",

    "Grid/3D": "true",
    "Grid/CellSize": "0.02",                     # Fine 2cm resolution
    "Grid/RangeMax": "10.0",
    "Grid/MaxObstacleHeight": "2.0",

    "Optimizer/Strategy": "1",
    "Optimizer/Iterations": "30",

    "Rtabmap/SaveWMState": "true",
}

# CONFIGURATION 3: Minimal/Fast (For testing)
params_minimal = {
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.3",
    "RGBD/AngularUpdate": "0.2",
    "RGBD/CreateOccupancyGrid": "true",

    "Vis/MaxFeatures": "200",
    "Vis/MinInliers": "10",

    "Grid/3D": "false",                          # Disable 3D grid
    "Rtabmap/DetectionRate": "1.0",
    "Rtabmap/SaveWMState": "true",
}

# CONFIGURATION 4: Loop Closure Focused
params_loop_closure = {
    "Rtabmap/DetectionRate": "2.0",
    "Rtabmap/LoopThr": "0.11",
    "Rtabmap/LoopRatio": "0.0",

    "RGBD/Enabled": "true",
    "RGBD/CreateOccupancyGrid": "true",
    "RGBD/ProximityBySpace": "true",
    "RGBD/ProximityMaxGraphDepth": "50",
    "RGBD/LocalLoopDetectionSpace": "true",
    "RGBD/LinearUpdate": "0.1",
    "RGBD/AngularUpdate": "0.1",

    "Vis/MaxFeatures": "1000",
    "Vis/MinInliers": "20",

    "Mem/RehearsalSimilarity": "0.6",
    "Mem/IncrementalMemory": "true",
    "Mem/STMSize": "10",

    "Grid/3D": "true",
    "Rtabmap/SaveWMState": "true",
}

# ===========================
# SELECT YOUR CONFIGURATION
# ===========================
# Change this variable to try different configurations!
SELECTED_PARAMS = params_high_performance  # <-- Change this!

print(f"Using configuration: {[k for k,v in locals().items() if v is SELECTED_PARAMS][0]}")
print(f"Total parameters: {len(SELECTED_PARAMS)}")
print("\nActive parameters:")
for key, value in SELECTED_PARAMS.items():
    print(f"  {key}: {value}")
print("=" * 80)

# ===========================
# PIPELINE SETUP
# ===========================

with dai.Pipeline() as p:
    fps = 30
    width = 640
    height = 400

    # Define sources and outputs
    left = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=fps)
    right = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=fps)
    imu = p.create(dai.node.IMU)
    stereo = p.create(dai.node.StereoDepth)
    featureTracker = p.create(dai.node.FeatureTracker)
    odom = p.create(dai.node.RTABMapVIO)
    slam = p.create(dai.node.RTABMapSLAM)

    # Apply selected RTAB-Map parameters
    slam.setParams(SELECTED_PARAMS)

    # IMU Configuration
    imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)

    # Feature Tracker Configuration
    featureTracker.setHardwareResources(1, 2)
    featureTracker.initialConfig.setCornerDetector(dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS)
    featureTracker.initialConfig.setCornerDetector(dai.FeatureTrackerConfig.CornerDetector.Type.value)

    featureTracker.initialConfig.setNumTargetFeatures(1000)
    featureTracker.initialConfig.setMotionEstimator(False)
    featureTracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

    # Stereo Depth Configuration
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

    # Create output queue for SLAM transformation data
    slamTransformQueue = slam.transform.createOutputQueue(maxSize=1, blocking=False)

    # Setup matplotlib for real-time visualization
    plt.ion()
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('RTAB-Map SLAM - Real-Time 3D Trajectory')

    # Data storage for trajectory
    trajectory_x = []
    trajectory_y = []
    trajectory_z = []

    p.start()

    print("\nDepthAI SLAM Pipeline Started - Logging SLAM Transformations")
    print("=" * 80)
    print(f"{'Timestamp':<25} {'X':<10} {'Y':<10} {'Z':<10} {'Qw':<8} {'Qx':<8} {'Qy':<8} {'Qz':<8}")
    print("-" * 80)

    frame_count = 0

    while p.isRunning():
        try:
            # Get SLAM transformation data
            if slamTransformQueue.has():
                transform = slamTransformQueue.get()

                # Extract transformation data with current device time
                timestamp = dai.Clock.now()

                # Get translation (position)
                translation = transform.getTranslation()
                x, y, z = translation.x, translation.y, translation.z

                # Get rotation (quaternion)
                quaternion = transform.getQuaternion()
                qw, qx, qy, qz = quaternion.qw, quaternion.qx, quaternion.qy, quaternion.qz

                # Log transformation data
                print(f"{timestamp!s:<25} {x:<10.4f} {y:<10.4f} {z:<10.4f} {qw:<8.4f} {qx:<8.4f} {qy:<8.4f} {qz:<8.4f}")

                # Store trajectory data
                trajectory_x.append(x)
                trajectory_y.append(y)
                trajectory_z.append(z)

                # Update visualization every 5 frames to reduce overhead
                frame_count += 1
                if frame_count % 5 == 0:
                    ax.clear()
                    ax.set_xlabel('X (m)')
                    ax.set_ylabel('Y (m)')
                    ax.set_zlabel('Z (m)')
                    ax.set_title(f'RTAB-Map SLAM - 3D Trajectory ({len(trajectory_x)} points)')

                    if len(trajectory_x) > 0:
                        # Plot trajectory line
                        ax.plot(trajectory_x, trajectory_y, trajectory_z, 'b-', linewidth=1, alpha=0.6)

                        # Plot current position as red dot
                        ax.scatter([x], [y], [z], c='r', marker='o', s=100, label='Current Position')

                        # Plot start position as green dot
                        if len(trajectory_x) > 1:
                            ax.scatter([trajectory_x[0]], [trajectory_y[0]], [trajectory_z[0]],
                                     c='g', marker='o', s=100, label='Start Position')

                        # Auto-scale with some margin
                        if len(trajectory_x) > 1:
                            x_range = max(trajectory_x) - min(trajectory_x)
                            y_range = max(trajectory_y) - min(trajectory_y)
                            z_range = max(trajectory_z) - min(trajectory_z)

                            margin = 0.1
                            ax.set_xlim([min(trajectory_x) - margin, max(trajectory_x) + margin])
                            ax.set_ylim([min(trajectory_y) - margin, max(trajectory_y) + margin])
                            ax.set_zlim([min(trajectory_z) - margin, max(trajectory_z) + margin])

                        ax.legend()
                        ax.grid(True)

                    plt.draw()
                    plt.pause(0.001)

        except Exception as e:
            print(f"Error reading SLAM transformation data: {e}")

        time.sleep(0.01)  # Small delay to prevent excessive CPU usage

    plt.ioff()
    plt.show()
