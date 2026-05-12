import time
import depthai as dai

# Create pipeline
with dai.Pipeline() as p:
    fps = 60
    width = 640
    height = 400
    
    # Define sources and outputs
    left = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=fps)
    right = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=fps)
    imu = p.create(dai.node.IMU)
    stereo = p.create(dai.node.StereoDepth)
    featureTracker = p.create(dai.node.FeatureTracker)
    odom = p.create(dai.node.RTABMapVIO)
    
    # IMU configuration
    imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)
    
    # Feature tracker configuration
    featureTracker.setHardwareResources(1, 2)
    featureTracker.initialConfig.setCornerDetector(dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS)
    featureTracker.initialConfig.setNumTargetFeatures(1000)
    featureTracker.initialConfig.setMotionEstimator(False)
    featureTracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49
    
    # Stereo configuration
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
    featureTracker.outputFeatures.link(odom.features)
    imu.out.link(odom.imu)
    
    # Create output queue for transformation data logging with smaller buffer
    transformQueue = odom.transform.createOutputQueue(maxSize=1, blocking=False)
    
    # Start pipeline
    p.start()
    
    print("DepthAI Pipeline Started - Logging Camera Transformations")
    print("=" * 60)
    print(f"{'Timestamp':<25} {'X':<10} {'Y':<10} {'Z':<10} {'Qw':<8} {'Qx':<8} {'Qy':<8} {'Qz':<8}")
    print("-" * 75)
    
    while p.isRunning():
        try:
            # Get transformation data
            if transformQueue.has():
                transform = transformQueue.get()
                # Extract transformation data with current device time (RTABMapVIO doesn't populate timestamps)
                timestamp = dai.Clock.now()

                # Get translation (position)
                translation = transform.getTranslation()
                x, y, z = translation.x, translation.y, translation.z

                # Get rotation (quaternion)
                quaternion = transform.getQuaternion()
                qw, qx, qy, qz = quaternion.qw, quaternion.qx, quaternion.qy, quaternion.qz

                # Log transformation data
                print(f"{timestamp!s:<25} {x:<10.4f} {y:<10.4f} {z:<10.4f} {qw:<8.4f} {qx:<8.4f} {qy:<8.4f} {qz:<8.4f}")
                
        except Exception as e:
            print(f"Error reading transformation data: {e}")
            
        time.sleep(0.01)  # Small delay to prevent excessive CPU usage