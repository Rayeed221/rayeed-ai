import time
import depthai as dai
import matplotlib.pyplot as plt

# Create pipeline

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

    params = {"RGBD/CreateOccupancyGrid": "true",
              "Grid/3D": "true",
              "Rtabmap/SaveWMState": "true"}
    slam.setParams(params)

    imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)

    featureTracker.setHardwareResources(1,2)
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

    print("DepthAI SLAM Pipeline Started - Logging SLAM Transformations")
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