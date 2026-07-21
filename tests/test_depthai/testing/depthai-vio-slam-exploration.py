import locale
locale.setlocale(locale.LC_NUMERIC, "C")   # force "." decimal separator for RTAB-Map C++ param parsing

import time
import cv2
import numpy as np
import depthai as dai

FPS    = 30
WIDTH  = 640
HEIGHT = 400

with dai.Pipeline() as p:

    # ── Cameras (v3: unified Camera.build) ────────────────────────────────────
    left  = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=FPS)
    right = p.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=FPS)

    # ── IMU ───────────────────────────────────────────────────────────────────
    imu = p.create(dai.node.IMU)
    imu.enableIMUSensor(
        [dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 200
    )
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)

    # ── Stereo depth ──────────────────────────────────────────────────────────
    stereo = p.create(dai.node.StereoDepth)
    stereo.setExtendedDisparity(False)
    stereo.setLeftRightCheck(True)
    stereo.setRectifyEdgeFillColor(0)
    stereo.enableDistortionCorrection(True)
    stereo.initialConfig.setLeftRightCheckThreshold(10)
    stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)  # align to left frame

    left.requestOutput((WIDTH, HEIGHT)).link(stereo.left)
    right.requestOutput((WIDTH, HEIGHT)).link(stereo.right)

    # ── Feature tracker ───────────────────────────────────────────────────────
    tracker = p.create(dai.node.FeatureTracker)
    tracker.setHardwareResources(1, 2)
    tracker.initialConfig.setCornerDetector(
        dai.FeatureTrackerConfig.CornerDetector.Type.HARRIS
    )
    tracker.initialConfig.setNumTargetFeatures(1000)
    tracker.initialConfig.setMotionEstimator(False)
    tracker.initialConfig.FeatureMaintainer.minimumDistanceBetweenFeatures = 49

    stereo.rectifiedLeft.link(tracker.inputImage)

    # ── VIO node ──────────────────────────────────────────────────────────────
    vio = p.create(dai.node.RTABMapVIO)
    vio.setUseFeatures(True)
# ─────────────────────────────────────────────────────────────────
#  vio.setParams()  — all RTABMap parameters consumed by RTABMapVIO
#  (rtabmap::Odometry::create() + visual/ICP registration stack)
# ─────────────────────────────────────────────────────────────────
    vio.setParams({

        # ── Odom core ────────────────────────────────────────────────
        "Odom/Strategy":               "0",     # 0=F2M 1=F2F 2=Fovis 3=viso2 4=DVO 5=ORB_SLAM2 6=OKVIS 9=VINS 10=OpenVINS
        "Odom/ResetCountdown":         "0",     # frames before auto-reset (0=never)
        "Odom/GuessMotion":            "1",     # constant-velocity motion prior (default 0)
        "Odom/GuessSmoothingDelay":    "0.0",   # seconds to delay applying motion guess
        "Odom/Holonomic":              "1",     # 1=full 6-DOF  0=non-holonomic (car)
        "Odom/FillInfoData":           "1",     # fill OdometryInfo for debugging
        "Odom/ImageBufferSize":        "0",     # input queue depth (0=unlimited)
        "Odom/AlignWithGround":        "0",     # align first pose with ground plane
        "Odom/ScanKeyFrameThr":        "0.9",   # scan overlap ratio for new keyframe
        "Odom/FlowWinSize":            "16",    # Lucas-Kanade optical flow window
        "Odom/FlowIterations":         "30",
        "Odom/FlowEps":                "0.01",
        "Odom/FlowMaxLevel":           "3",     # pyramid levels for optical flow

        # ── Visual registration (Vis) ─────────────────────────────────
        "Vis/EstimationType":          "0",     # 0=PnP(3D→2D)  1=Essential(2D→2D)  2=ICP(3D→3D)
        "Vis/ForwardEstOnly":          "1",     # estimate only forward motion
        "Vis/FeatureType":             "8",     # 0=SURF 1=SIFT 2=ORB 3=FAST/FREAK 4=FAST/BRIEF
                                                # 5=GFTT/FREAK 6=GFTT/BRIEF 7=BRISK
                                                # 8=GFTT/ORB 9=KAZE 10=ORB-OCTREE 11=SuperPoint
                                                # 12=SURF/FREAK 13=GFTT/DAISY 14=SURF/DAISY
        "Vis/MaxFeatures":             "600",   # max keypoints per frame (default 1000)
        "Vis/MinInliers":              "15",    # RANSAC inliers to accept pose (default 20)
        "Vis/InlierDistance":          "0.1",   # max 3D distance (m) for inlier (default 0.1)
        "Vis/Iterations":              "300",   # RANSAC iterations (default 300)
        "Vis/RefineIterations":        "10",    # refinement iterations after RANSAC
        "Vis/MaxRANSACIterations":     "0",     # hard cap on RANSAC (0=use Iterations)
        "Vis/MaxDepth":                "4.0",   # max feature depth in metres (default 0=inf)
        "Vis/MinDepth":                "0.3",   # min feature depth in metres (default 0)
        "Vis/DepthAsMask":             "1",     # mask features where depth is invalid
        "Vis/CorType":                 "0",     # 0=feature matching  1=optical flow
        "Vis/CorNNType":               "1",     # 0=BruteForce 1=FLANN_KDTREE 2=FLANN_LSH
                                                # 3=BruteForce_GPU 4=BruteForce_GPU_NMSM
        "Vis/CorNNDR":                 "0.8",   # descriptor ratio test (default 0.8)
        "Vis/CorGuessWinSize":         "40",    # px search window around motion prediction
        "Vis/CorFlowWinSize":          "16",    # optical-flow correlation window
        "Vis/CorFlowIterations":       "30",
        "Vis/CorFlowEps":              "0.01",
        "Vis/CorFlowMaxLevel":         "3",
        "Vis/PnPReprojError":          "2.0",   # RANSAC reprojection error in px (default 8)
        "Vis/PnPFlags":                "0",     # 0=iterative  1=EPnP  2=P3P
        "Vis/PnPRefineIterations":     "1",
        "Vis/EpipolarGeometryVar":     "0.02",  # epipolar variance (EstimationType=1 only)
        "Vis/SubPixWinSize":           "3",     # sub-pixel refinement window
        "Vis/SubPixIterations":        "0",     # 0=disabled
        "Vis/SubPixEps":               "0.02",
        "Vis/RoiRatios":               "0.0 0.0 0.0 0.0",  # "top bot left right" crop ratio
        "Vis/BundleAdjustment":        "0",     # 0=none 1=g2o 2=cvsba 3=Ceres 4=GTSAM

        # ── Frame-to-Map odometry (Odom/Strategy=0) ───────────────────
        "OdometryF2M/MaxSize":                 "1000",  # max 3D points in local map
        "OdometryF2M/BundleAdjustment":        "0",     # BA on local map (0=off)
        "OdometryF2M/BundleAdjustmentMaxFrames":"0",    # frames in BA window (0=all)
        "OdometryF2M/ScanMaxSize":             "0",     # max scan points (0=unlimited)
        "OdometryF2M/ScanSubtractRadius":      "0.05",  # voxel radius for scan subtraction
        "OdometryF2M/ScanSubtractAngle":       "0.0",   # angle constraint for subtraction
        "OdometryF2M/FixedMapPath":            "",      # load static map from file

        # ── Frame-to-Frame odometry (Odom/Strategy=1) ─────────────────
        "OdometryF2F/KeyFrameThr":     "0.3",   # new keyframe when inlier ratio < this
        "OdometryF2F/ScanKeyFrameThr": "0.9",   # scan variant of above

        # ── Registration strategy ──────────────────────────────────────
        "Reg/Strategy":                "0",     # 0=Visual  1=ICP  2=Visual+ICP
        "Reg/Force3DoF":               "0",     # MUST be 0 for drone
        "Reg/RepeatOnce":              "1",     # retry registration once on failure

        # ── ICP registration (Reg/Strategy=1 or 2) ────────────────────
        "Icp/Strategy":                "1",     # 0=libpointmatcher  1=PCL  2=Open3D
        "Icp/MaxTranslation":          "0.2",   # reject if Δt > this (m)
        "Icp/MaxRotation":             "0.78",  # reject if Δr > this (rad)
        "Icp/MaxCorrespondenceDistance":"0.05", # max point-pair distance (m)
        "Icp/VoxelSize":               "0.05",  # downsample voxel size (m)  0=off
        "Icp/DownsamplingStep":        "1",     # scan decimation step
        "Icp/Iterations":              "30",
        "Icp/Epsilon":                 "0.001", # convergence delta
        "Icp/CorrespondenceRatio":     "0.1",   # min inlier ratio to accept
        "Icp/PointToPlane":            "1",     # 0=point-to-point  1=point-to-plane
        "Icp/PointToPlaneK":           "5",     # neighbours for normal estimation
        "Icp/PointToPlaneRadius":      "0.0",   # radius for normal estimation (0=use K)
        "Icp/PointToPlaneGroundNormalsUp": "0.0",# constrain ground normals upward
        "Icp/ReciprocalCorrespondences":"0",    # enforce bidirectional pairing
        "Icp/OutlierRatio":            "0.85",  # max outlier fraction (libpointmatcher)
        "Icp/RangeMin":                "0.0",   # min scan range (m)
        "Icp/RangeMax":                "0.0",   # max scan range (m)  0=unlimited
        "Icp/FiltersEnabled":          "1",     # enable libpointmatcher filter chain
        "Icp/PMMatcherFactor":         "1.0",
        "Icp/PMMatcherMaxDist":        "0.0",
        "Icp/PMMatcherKnn":            "1",

    })

    tracker.passthroughInputImage.link(vio.rect)
    stereo.depth.link(vio.depth)
    tracker.outputFeatures.link(vio.features)
    imu.out.link(vio.imu)

    # ── SLAM node ─────────────────────────────────────────────────────────────
    slam = p.create(dai.node.RTABMapSLAM)
    slam.setFreq(2.0)
    slam.setAlphaScaling(-1.0)
    slam.setDatabasePath("./map.db")
    slam.setLoadDatabaseOnStart(False)
    slam.setSaveDatabaseOnClose(True)
    slam.setSaveDatabasePeriodically(True)
    slam.setSaveDatabasePeriod(60.0)
    slam.setPublishGrid(True)
    slam.setPublishGroundCloud(True)
    slam.setPublishObstacleCloud(True)
# ─────────────────────────────────────────────────────────────────
#  slam.setParams()  — all RTABMap parameters consumed by RTABMapSLAM
#  (rtabmap.init() + OccupancyGrid() + CloudMap())
# ─────────────────────────────────────────────────────────────────
    slam.setParams({

        # ── RTABMap core ──────────────────────────────────────────────
        "Rtabmap/DetectionRate":              "1.0",   # Hz — mirror slam.setFreq()
        "Rtabmap/TimeThr":                    "0.0",   # max ms per cycle (0=unlimited)
        "Rtabmap/MemoryThr":                  "0",     # max WM nodes (0=unlimited)
        "Rtabmap/LoopThr":                    "0.11",  # loop closure similarity threshold
        "Rtabmap/LoopRatio":                  "0.0",   # best/second-best ratio gate
        "Rtabmap/MaxRetrieved":               "2",     # max WM nodes retrieved per cycle
        "Rtabmap/ImageDecimation":            "1",     # downsample images before SLAM
        "Rtabmap/ImagesAlreadyRectified":     "1",     # skip internal rectification
        "Rtabmap/CreateIntermediateNodes":    "0",     # store odometry-only nodes in graph
        "Rtabmap/StartNewMapOnLoopClosure":   "0",     # start fresh map after first loop
        "Rtabmap/StartNewMapOnGoodSignature": "0",
        "Rtabmap/PublishStats":               "1",
        "Rtabmap/PublishLastSignature":       "1",
        "Rtabmap/PublishRAMUsage":            "0",
        "Rtabmap/ComputeRMSE":                "0",
        "Rtabmap/SaveWMState":                "0",
        "Rtabmap/StatisticLogged":            "0",
        "Rtabmap/StatisticLoggedHeaders":     "0",

        # ── RGBD ──────────────────────────────────────────────────────
        "RGBD/Enabled":                       "1",
        "RGBD/LinearUpdate":                  "0.1",   # min Δt (m) to add keyframe
        "RGBD/AngularUpdate":                 "0.1",   # min Δr (rad) to add keyframe
        "RGBD/LinearSpeedUpdate":             "0.0",   # min linear speed trigger (m/s)
        "RGBD/AngularSpeedUpdate":            "0.0",   # min angular speed trigger (rad/s)
        "RGBD/NewMapOdomChangeDistance":      "0.0",   # start new map after Δt (0=off)
        "RGBD/OptimizeFromGraphEnd":          "0",     # 0=anchor at origin  1=anchor at end
        "RGBD/OptimizeMaxError":              "3.0",   # reject loop if optimiser error > this
        "RGBD/ForceOdom3DoF":                 "0",     # force planar odom (0 for drone)
        "RGBD/CreateOccupancyGrid":           "1",     # build grid inside SLAM node
        "RGBD/SavedLocalizationIgnored":      "0",
        "RGBD/StartAtOrigin":                 "0",
        "RGBD/MaxLocalRetrieved":             "10",    # WM nodes recalled per cycle
        "RGBD/MaxOdomCacheSize":              "10",    # odom frames buffered between keyframes
        "RGBD/LoopClosureReextractFeatures":  "0",     # re-extract features on loop closure
        "RGBD/NeighborLinkRefining":          "0",     # refine odometry edges in graph
        "RGBD/LocalRadius":                   "10.0",  # local map radius (m)
        "RGBD/LocalImmunizationRatio":        "0.25",
        "RGBD/MarkerDetection":               "0",     # ArUco/ChArUco marker detection

        # RGBD proximity (space-based loop closure) ───────────────────
        "RGBD/ProximityBySpace":              "1",     # space-based proximity detection
        "RGBD/ProximityByTime":               "0",     # time-based proximity detection
        "RGBD/ProximityMaxGraphDepth":        "0",     # graph traversal depth (0=unlimited)
        "RGBD/ProximityMaxPaths":             "3",     # max paths explored per cycle
        "RGBD/ProximityPathMaxNeighbors":     "10",    # candidates per proximity step
        "RGBD/ProximityPathScansMerged":      "0",     # merge scans along proximity path
        "RGBD/ProximityFilteringRadius":      "1.0",   # spatial filter radius (m)
        "RGBD/ProximityAngle":                "45.0",  # max angle between proximity nodes
        "RGBD/ProximityOdomGuess":            "0",     # use odom as proximity initial guess
        "RGBD/ProximityMaxDepth":             "-1",    # max proximity path depth (-1=auto)

        # ── Memory management ─────────────────────────────────────────
        "Mem/STMSize":                        "10",    # short-term memory node count
        "Mem/IncrementalMemory":              "1",     # 1=mapping  0=localisation only
        "Mem/InitWMWithAllNodes":             "0",     # load all DB nodes into WM at start
        "Mem/RehearsalSimilarity":            "0.30",  # STM consolidation threshold
        "Mem/RehearsalIdUpdatedToNewOne":     "0",
        "Mem/ImageKept":                      "1",     # store images in DB
        "Mem/BinDataKept":                    "1",     # store binary descriptors in DB
        "Mem/RawDescriptorsKept":             "1",     # keep raw descriptors
        "Mem/MapLabelsAdded":                 "1",
        "Mem/SaveDepth16Format":              "0",     # save depth as 16-bit PNG
        "Mem/NotLinkedNodesKept":             "1",
        "Mem/TransferSortingByWeightId":      "0",
        "Mem/GenerateIds":                    "1",
        "Mem/BadSignaturesIgnored":           "0",
        "Mem/UseOdomGravity":                 "0",     # fuse IMU gravity into graph
        "Mem/DepthAsMask":                    "1",
        "Mem/ImagePreDecimation":             "1",     # decimate before feature extraction
        "Mem/ImagePostDecimation":            "1",     # decimate before DB storage
        "Mem/IntermediateNodeDataKept":       "1",
        "Mem/LocalizationDataSaved":          "0",
        "Mem/CovOffDiagIgnored":              "1",     # ignore off-diagonal covariance
        "Mem/GTPoseIgnored":                  "1",
        "Mem/CompressionParallelized":        "1",
        "Mem/LaserScanDownsampleStepSize":    "1",
        "Mem/LaserScanVoxelSize":             "0.0",
        "Mem/LaserScanNormalK":               "0",
        "Mem/LaserScanNormalRadius":          "0.0",

        # ── Keypoints / vocabulary ────────────────────────────────────
        "Kp/DetectorStrategy":                "8",     # must match Vis/FeatureType
        "Kp/MaxFeatures":                     "500",   # vocab features per node
        "Kp/NNStrategy":                      "1",     # 0=BruteForce  1=FLANN_KDTREE  2=FLANN_LSH
        "Kp/NndrRatio":                       "0.8",   # nearest-neighbour distance ratio
        "Kp/BadSignRatio":                    "0.5",   # discard node if inlier ratio < this
        "Kp/WordThr":                         "0",     # min word count to accept signature
        "Kp/TfIdfLikelihoodUsed":             "1",     # TF-IDF weighting for place recognition
        "Kp/Parallelized":                    "1",     # parallel feature extraction
        "Kp/RoiRatios":                       "0.0 0.0 0.0 0.0",
        "Kp/MaxDepth":                        "0.0",   # feature depth filter (0=off)
        "Kp/MinDepth":                        "0.0",
        "Kp/SubPixWinSize":                   "3",
        "Kp/SubPixIterations":                "0",
        "Kp/SubPixEps":                       "0.02",
        "Kp/GridRows":                        "1",     # divide image into grid for uniform kp
        "Kp/GridCols":                        "1",
        "Kp/DictionaryPath":                  "",      # custom BoW dictionary file
        "Kp/NewWordsComparedTogether":        "1",

        # ── Occupancy grid ────────────────────────────────────────────
        "Grid/Sensor":                        "1",     # 0=scan  1=depth  2=both
        "Grid/CellSize":                      "0.05",  # metres per cell
        "Grid/RangeMin":                      "0.3",   # min depth included (m)
        "Grid/RangeMax":                      "4.0",   # max depth included (m)  0=unlimited
        "Grid/NormalsSegmentation":           "1",     # normal-based ground/obstacle split
        "Grid/MaxGroundAngle":                "45.0",  # max angle (deg) for ground normal
        "Grid/NormalK":                       "10",    # neighbours for normal estimation
        "Grid/MaxGroundHeight":               "0.1",   # points ≤ this → ground (m)
        "Grid/MinGroundHeight":               "-0.1",  # floor below sensor
        "Grid/MaxObstacleHeight":             "2.5",   # points above this discarded (m)
        "Grid/GroundIsObstacle":              "0",     # treat ground as obstacle
        "Grid/ClusterRadius":                 "0.1",   # obstacle cluster merge radius (m)
        "Grid/MinClusterSize":                "10",    # min points per obstacle cluster
        "Grid/NoiseFilteringRadius":          "0.05",  # statistical noise filter radius
        "Grid/NoiseFilteringMinNeighbors":    "2",
        "Grid/FootprintLength":               "0.3",   # drone body exclusion zone (m)
        "Grid/FootprintWidth":                "0.3",
        "Grid/FootprintHeight":               "0.15",
        "Grid/MapFrameProjection":            "0",     # project grid in map(1) or sensor(0) frame
        "Grid/3D":                            "1",     # 3D voxel grid (1) or 2D projection (0)
        "Grid/DepthDecimation":               "4",     # depth image decimation before grid
        "Grid/PreVoxelFiltering":             "1",     # voxel filter before segmentation
        "Grid/FromDepth":                     "1",     # build grid from depth (not scan)
        "Grid/FlatObstacleDetected":          "1",     # detect flat vertical obstacles
        "Grid/ScanDecimation":                "1",     # scan point decimation step
        "Grid/RayTracing":                    "0",     # ray-trace free space (expensive)
        # Probabilistic grid parameters (when Grid/RayTracing=1)
        "Grid/OccupancyThr":                  "0.5",
        "Grid/ProbHit":                       "0.7",
        "Grid/ProbMiss":                      "0.4",
        "Grid/ClampingThresMin":              "0.1192",
        "Grid/ClampingThresMax":              "0.971",
        "Grid/UpdateError":                   "0.01",

        # ── Pose graph optimiser ──────────────────────────────────────
        "Optimizer/Strategy":                 "1",     # 0=TORO  1=g2o  2=GTSAM  3=Ceres
        "Optimizer/Iterations":               "100",
        "Optimizer/Robust":                   "1",     # Huber/DCS kernel on loop edges
        "Optimizer/VarianceIgnored":          "0",     # ignore edge covariances
        "Optimizer/LandmarksIgnored":         "0",     # ignore landmark nodes in graph
        "Optimizer/Epsilon":                  "0.0001",# convergence threshold
        "Optimizer/GravitySigma":             "0.3",   # IMU gravity constraint sigma (GTSAM)
        "Optimizer/PriorsIgnored":            "1",
        "Optimizer/InvalidMax":               "0",     # max invalid edges before abort

        # ── Visual registration for loop closure ──────────────────────
        # (same Vis/* and Reg/* namespaces — override here for LC quality vs speed)
        "Vis/MinInliers":                     "15",
        "Vis/MaxDepth":                       "4.0",
        "Vis/MinDepth":                       "0.3",
        "Vis/MaxFeatures":                    "500",
        "Vis/FeatureType":                    "8",
        "Reg/Strategy":                       "0",
        "Reg/Force3DoF":                      "0",
        "Reg/RepeatOnce":                     "1",

        # ── ICP for loop closure refinement (Reg/Strategy=2) ─────────
        "Icp/Strategy":                       "1",
        "Icp/MaxTranslation":                 "0.2",
        "Icp/MaxRotation":                    "0.78",
        "Icp/VoxelSize":                      "0.05",
        "Icp/Iterations":                     "30",
        "Icp/CorrespondenceRatio":            "0.1",
        "Icp/PointToPlane":                   "1",
        "Icp/PointToPlaneK":                  "5",
        "Icp/OutlierRatio":                   "0.85",
        "Icp/RangeMin":                       "0.3",
        "Icp/RangeMax":                       "4.0",

    })
    vio.transform.link(slam.odom)
    vio.passthroughRect.link(slam.rect)
    vio.passthroughDepth.link(slam.depth)

    # ── Output queues (v3: createOutputQueue directly on node output) ─────────
    # Both passthrough outputs are already linked to SLAM above — v3 allows
    # creating a queue on the same output simultaneously.
    q_rect      = vio.passthroughRect.createOutputQueue(maxSize=4, blocking=False)
    q_depth     = vio.passthroughDepth.createOutputQueue(maxSize=4, blocking=False)
    q_transform = vio.transform.createOutputQueue(maxSize=1, blocking=False)

    # ── Start ─────────────────────────────────────────────────────────────────
    p.start()
    print("Pipeline running — press 'q' to quit")

    pose_str = "Pose: waiting..."

    while p.isRunning():
        # -- VIO transform (console HUD data) ----------------------------------
        if q_transform.has():
            tf = q_transform.get()
            t  = tf.getTranslation()
            q  = tf.getQuaternion()
            pose_str = (
                f"Pose  x={t.x:+.3f}  y={t.y:+.3f}  z={t.z:+.3f} m  "
                f"qw={q.qw:.3f}  qx={q.qx:.3f}  qy={q.qy:.3f}  qz={q.qz:.3f}"
            )
            print(pose_str)

        # -- Rectified left frame ----------------------------------------------
        if q_rect.has():
            frame = q_rect.get().getCvFrame()
            if frame.ndim == 2:                        # mono → BGR for overlays
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            # HUD: active VIO parameters
            hud = [
                "VIO: F2M | GFTT+ORB",
                f"MaxFeat=600  MinInliers=15",
                f"Depth 0.3-4.0 m  F2M size=1000",
                pose_str[:72],
            ]
            for i, line in enumerate(hud):
                cv2.putText(
                    frame, line, (8, 20 + i * 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 0), 1, cv2.LINE_AA
                )
            cv2.imshow("Rectified Left — VIO passthrough", frame)

        # -- Depth frame -------------------------------------------------------
        if q_depth.has():
            depth_raw = q_depth.get().getFrame()        # uint16, mm
            # Clamp to 300–4000 mm (matching Vis/MinDepth and Vis/MaxDepth)
            depth_clamped = np.clip(depth_raw, 300, 4000).astype(np.float32)
            depth_norm = ((depth_clamped - 300) / (4000 - 300) * 255).astype(np.uint8)
            depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_JET)

            # Mark invalid pixels (0 / 65535) black
            invalid = (depth_raw == 0) | (depth_raw == 65535)
            depth_color[invalid] = 0

            cv2.putText(
                depth_color, "Depth  0.3 m [blue] → 4.0 m [red]",
                (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA
            )
            cv2.imshow("Depth — VIO passthrough", depth_color)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.005)

cv2.destroyAllWindows()
