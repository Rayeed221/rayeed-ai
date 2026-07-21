"""
RTAB-Map Parameter Exploration for DepthAI v3
==============================================
This file demonstrates various RTAB-Map parameters that can be used with
the RTABMapSLAM node in DepthAI v3.

Reference: https://github.com/introlab/rtabmap/blob/master/corelib/include/rtabmap/core/Parameters.h
"""

import time
import depthai as dai

# ===========================
# PARAMETER CONFIGURATIONS
# ===========================

# BASIC CONFIGURATION (Your current setup)
params_basic = {
    "RGBD/CreateOccupancyGrid": "true",  # Create 2D occupancy grid
    "Grid/3D": "true",                    # Create 3D occupancy grid
    "Rtabmap/SaveWMState": "true"         # Save working memory state
}

# PERFORMANCE OPTIMIZED (For faster processing)
params_performance = {
    # Core SLAM Settings
    "Rtabmap/DetectionRate": "2.0",              # Detection rate in Hz (higher = more loop closures)
    "Rtabmap/TimeThr": "0",                      # Max time for map update (0 = infinity)
    "Rtabmap/MemoryThr": "300",                  # Max nodes in working memory
    "Rtabmap/LoopThr": "0.11",                   # Loop closure threshold (lower = more strict)

    # RGBD Settings
    "RGBD/Enabled": "true",                      # Enable RGB-D SLAM mode
    "RGBD/LinearUpdate": "0.1",                  # Min linear movement to add node (meters)
    "RGBD/AngularUpdate": "0.1",                 # Min angular movement to add node (radians)
    "RGBD/OptimizeFromGraphEnd": "false",        # Optimize from last node
    "RGBD/CreateOccupancyGrid": "true",          # Enable occupancy grid creation

    # Visual Features
    "Vis/MaxFeatures": "500",                    # Max features per image
    "Vis/MinInliers": "15",                      # Min inliers for valid transform
    "Vis/InlierDistance": "0.1",                 # Max inlier distance (meters)
    "Vis/EstimationType": "0",                   # 0=3D-3D, 1=PnP, 2=Epipolar

    # Optimizer Settings
    "Optimizer/Strategy": "1",                   # 0=TORO, 1=g2o, 2=GTSAM, 3=Ceres
    "Optimizer/Iterations": "20",                # Number of optimization iterations
    "Optimizer/Robust": "false",                 # Use robust optimization (Vertigo)

    # Grid Settings
    "Grid/3D": "true",                           # Enable 3D grid
    "Grid/CellSize": "0.05",                     # Grid cell size (meters)
    "Grid/RangeMax": "5.0",                      # Max range for obstacles (meters)
    "Grid/ClusterRadius": "0.1",                 # Cluster radius for filtering
}

# HIGH ACCURACY (For detailed mapping, slower)
params_high_accuracy = {
    # Core SLAM
    "Rtabmap/DetectionRate": "1.0",              # Lower rate for more processing time
    "Rtabmap/MemoryThr": "0",                    # Unlimited working memory
    "Rtabmap/TimeThr": "700",                    # Max 700ms for map update
    "Rtabmap/LoopThr": "0.15",                   # Higher threshold = less strict

    # RGBD Settings
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.05",                 # More frequent updates
    "RGBD/AngularUpdate": "0.05",                # More frequent angular updates
    "RGBD/OptimizeMaxError": "3.0",              # Max optimization error before rejection
    "RGBD/MaxLoopClosureDistance": "0.0",        # No distance limit
    "RGBD/LocalRadius": "10.0",                  # Local map radius (meters)
    "RGBD/NeighborLinkRefining": "true",         # Refine neighbor links
    "RGBD/ProximityBySpace": "true",             # Use spatial proximity

    # Visual Features (High detail)
    "Vis/MaxFeatures": "1000",                   # Extract more features
    "Vis/MinInliers": "20",                      # Require more inliers
    "Vis/InlierDistance": "0.05",                # Stricter inlier distance
    "Vis/CorrespondenceType": "0",               # 0=Features, 1=Optical Flow

    # Feature Detector Settings
    "Kp/MaxFeatures": "1000",                    # Max keypoints to extract
    "Kp/DetectorStrategy": "6",                  # 0=SURF, 6=GFTT, 8=ORB, 9=FAST
    "Kp/NndrRatio": "0.8",                       # NNDR ratio for matching

    # GFTT (Good Features To Track) Settings
    "GFTT/QualityLevel": "0.001",                # Corner quality level
    "GFTT/MinDistance": "7.0",                   # Min distance between features

    # Grid Settings (High resolution)
    "Grid/3D": "true",
    "Grid/CellSize": "0.02",                     # Finer grid resolution
    "Grid/RangeMax": "10.0",                     # Larger detection range
    "Grid/ClusterRadius": "0.05",
    "Grid/GroundIsObstacle": "false",            # Don't treat ground as obstacle
    "Grid/MaxObstacleHeight": "2.0",             # Max obstacle height (meters)
    "Grid/MinGroundHeight": "-0.1",              # Min ground height (meters)
}

# OUTDOOR/DRONE OPTIMIZED
params_outdoor_drone = {
    # Core SLAM
    "Rtabmap/DetectionRate": "3.0",              # Higher rate for fast movement
    "Rtabmap/MemoryThr": "200",                  # Moderate memory
    "Rtabmap/TimeThr": "0",                      # No time limit

    # RGBD Settings (Adapted for outdoor)
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.2",                  # Larger movement threshold
    "RGBD/AngularUpdate": "0.15",                # Larger rotation threshold
    "RGBD/LocalRadius": "15.0",                  # Larger local map for outdoor
    "RGBD/MaxLoopClosureDistance": "15.0",       # Allow distant loop closures

    # Visual Features (Robust to lighting changes)
    "Vis/MaxFeatures": "800",
    "Vis/MinInliers": "15",
    "Vis/InlierDistance": "0.15",                # More tolerance for outdoor

    # Feature Detector (Fast and robust)
    "Kp/MaxFeatures": "800",
    "Kp/DetectorStrategy": "8",                  # ORB is good for outdoor

    # ORB Settings
    "ORB/ScaleFactor": "1.2",                    # Pyramid decimation ratio
    "ORB/NLevels": "8",                          # Number of pyramid levels
    "ORB/EdgeThreshold": "19",                   # Border size

    # Grid Settings (Outdoor environment)
    "Grid/3D": "true",
    "Grid/CellSize": "0.1",                      # Coarser for speed
    "Grid/RangeMax": "20.0",                     # Large detection range
    "Grid/MaxObstacleHeight": "3.0",             # Higher obstacles (trees, etc.)
    "Grid/GroundIsObstacle": "false",

    # IMU Integration
    "Optimizer/GravitySigma": "0.3",             # Gravity constraint weight
}

# LOOP CLOSURE FOCUSED
params_loop_closure = {
    # Core Loop Closure Settings
    "Rtabmap/DetectionRate": "2.0",
    "Rtabmap/LoopThr": "0.11",                   # Loop closure threshold
    "Rtabmap/LoopRatio": "0.0",                  # Acceptance ratio
    "Rtabmap/LoopCounterIdThr": "3",             # Loop closure ID threshold
    "Rtabmap/LoopClosureReextractFeatures": "false",

    # RGBD Loop Closure
    "RGBD/Enabled": "true",
    "RGBD/ProximityBySpace": "true",             # Enable spatial proximity
    "RGBD/ProximityMaxGraphDepth": "50",         # Max graph depth for proximity
    "RGBD/ProximityPathMaxNeighbors": "10",      # Max neighbors in path
    "RGBD/LocalLoopDetectionSpace": "true",      # Local loop detection
    "RGBD/LocalLoopDetectionTime": "false",      # Disable time-based detection

    # Visual Loop Closure
    "Vis/MaxFeatures": "1000",
    "Vis/MinInliers": "20",

    # Memory Management for Loop Closure
    "Mem/RehearsalSimilarity": "0.6",            # Rehearsal threshold
    "Mem/IncrementalMemory": "true",             # SLAM mode
    "Mem/STMSize": "10",                         # Short-term memory size
    "Mem/BadSignaturesIgnored": "false",         # Keep bad signatures
}

# MINIMAL CONFIGURATION (Fastest, least accurate)
params_minimal = {
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.3",                  # Large movement threshold
    "RGBD/AngularUpdate": "0.2",
    "Vis/MaxFeatures": "200",                    # Minimal features
    "Vis/MinInliers": "10",
    "Grid/3D": "false",                          # Disable 3D grid for speed
    "Rtabmap/DetectionRate": "1.0",
}

# DATABASE AND SAVING OPTIONS
params_database = {
    "Rtabmap/SaveWMState": "true",               # Save working memory state
    "DbSqlite3/InMemory": "false",               # Use disk database
    "DbSqlite3/CacheSize": "10000",              # SQLite cache size
    "DbSqlite3/JournalMode": "WAL",              # Write-Ahead Logging
    "Mem/ImageKept": "true",                     # Keep raw images
    "Mem/ImageCompressionFormat": ".jpg",        # Image compression
}

# VISUALIZATION OPTIONS
params_visualization = {
    "RGBD/CreateOccupancyGrid": "true",          # Enable occupancy grid
    "Grid/3D": "true",                           # 3D grid
    "Grid/FromDepth": "true",                    # Create grid from depth
    "Grid/GroundIsObstacle": "false",
    "Grid/NormalsSegmentation": "true",          # Segment using normals
    "GridGlobal/MinSize": "20",                  # Global grid min size (meters)
}


def create_pipeline_with_params(param_config):
    """
    Create a DepthAI pipeline with specified RTAB-Map parameters

    Args:
        param_config: Dictionary of RTAB-Map parameters

    Returns:
        Configured DepthAI pipeline
    """
    pipeline = dai.Pipeline()

    # Define sources
    left = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=30)
    right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=30)
    imu = pipeline.create(dai.node.IMU)
    stereo = pipeline.create(dai.node.StereoDepth)
    featureTracker = pipeline.create(dai.node.FeatureTracker)
    odom = pipeline.create(dai.node.RTABMapVIO)
    slam = pipeline.create(dai.node.RTABMapSLAM)

    # Apply RTAB-Map parameters
    slam.setParams(param_config)

    # Configure IMU
    imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)

    # Configure feature tracker
    featureTracker.setHardwareResources(1, 2)
    featureTracker.initialConfig.setCornerDetector(dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS)
    featureTracker.initialConfig.setNumTargetFeatures(1000)
    featureTracker.initialConfig.setMotionEstimator(False)
    featureTracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

    # Configure stereo depth
    stereo.setExtendedDisparity(False)
    stereo.setLeftRightCheck(True)
    stereo.setRectifyEdgeFillColor(0)
    stereo.enableDistortionCorrection(True)
    stereo.initialConfig.setLeftRightCheckThreshold(10)
    stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)

    # Link nodes
    left.requestOutput((640, 400)).link(stereo.left)
    right.requestOutput((640, 400)).link(stereo.right)
    featureTracker.passthroughInputImage.link(odom.rect)
    stereo.rectifiedLeft.link(featureTracker.inputImage)
    stereo.depth.link(odom.depth)
    imu.out.link(odom.imu)
    featureTracker.outputFeatures.link(odom.features)

    odom.transform.link(slam.odom)
    odom.passthroughRect.link(slam.rect)
    odom.passthroughDepth.link(slam.depth)

    return pipeline


# ===========================
# USAGE EXAMPLE
# ===========================

if __name__ == "__main__":
    print("RTAB-Map Parameter Exploration Demo")
    print("=" * 60)
    print("\nAvailable parameter configurations:")
    print("1. params_basic - Your current configuration")
    print("2. params_performance - Optimized for speed")
    print("3. params_high_accuracy - Maximum accuracy (slower)")
    print("4. params_outdoor_drone - Optimized for outdoor/drone use")
    print("5. params_loop_closure - Focus on loop closure detection")
    print("6. params_minimal - Fastest, minimal accuracy")
    print("\nSelect a configuration or create your own by combining parameters!")
    print("\nExample: Create pipeline with outdoor drone parameters")
    print("pipeline = create_pipeline_with_params(params_outdoor_drone)")

    # Example: Use outdoor drone configuration
    # Uncomment to test:
    with create_pipeline_with_params(params_outdoor_drone) as pipeline:
        print("\nPipeline created with outdoor drone parameters")
        print("Starting pipeline...")
    #     # Your pipeline logic here
