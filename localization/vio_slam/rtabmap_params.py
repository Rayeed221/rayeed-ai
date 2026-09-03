"""
RTAB-Map parameter dicts for dai.node.RTABMapVIO and dai.node.RTABMapSLAM.

Tuned for a USB 2.0 link on a Raspberry Pi 5 (10 fps VIO / 2 Hz SLAM).

LOCKED INVARIANTS (do NOT change without coordinated re-tuning):

  - VIO_PARAMS["Odom/Strategy"]        == "0"   (F2M — best for drones)
  - VIO_PARAMS["Vis/FeatureType"]      == "8"   ┐ MUST match — GFTT+ORB
  - SLAM_PARAMS["Kp/DetectorStrategy"] == "8"   ┘
  - VIO_PARAMS["Reg/Force3DoF"]        == "0"   ┐ MUST be 0 for drone (6-DOF)
  - SLAM_PARAMS["RGBD/ForceOdom3DoF"]  == "0"   ┘
  - VIO_PARAMS["Vis/MaxDepth"]  == "4.0", VIO_PARAMS["Vis/MinDepth"] == "0.3"
  - SLAM_PARAMS["Grid/3D"]      == "1"   (required for slam.obstaclePCL output)
  - SLAM_PARAMS["Grid/CellSize"]== "0.05" MUST equal config.VIOSLAM_OCC_CELL_SIZE
  - SLAM_PARAMS["Rtabmap/DetectionRate"] == str(config.VIOSLAM_SLAM_HZ) and MUST
    equal slam.setFreq(); both MUST be <= config.VIOSLAM_FPS (frames arrive at fps)

All values are strings — RTABMap parses them itself.  Numeric values must use
"." as decimal separator regardless of locale (set LC_NUMERIC=C in the runner).
"""

VIO_PARAMS: dict = {

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
    "Vis/FeatureType":             "8",     # 8=GFTT/ORB (must match SLAM_PARAMS Kp/DetectorStrategy)
    "Vis/MaxFeatures":             "600",
    "Vis/MinInliers":              "15",
    "Vis/InlierDistance":          "0.1",
    "Vis/Iterations":              "300",
    "Vis/RefineIterations":        "10",
    "Vis/MaxRANSACIterations":     "0",
    "Vis/MaxDepth":                "4.0",
    "Vis/MinDepth":                "0.3",
    "Vis/DepthAsMask":             "1",
    "Vis/CorType":                 "0",
    "Vis/CorNNType":               "1",
    "Vis/CorNNDR":                 "0.8",
    "Vis/CorGuessWinSize":         "40",
    "Vis/CorFlowWinSize":          "16",
    "Vis/CorFlowIterations":       "30",
    "Vis/CorFlowEps":              "0.01",
    "Vis/CorFlowMaxLevel":         "3",
    "Vis/PnPReprojError":          "2.0",
    "Vis/PnPFlags":                "0",
    "Vis/PnPRefineIterations":     "1",
    "Vis/EpipolarGeometryVar":     "0.02",
    "Vis/SubPixWinSize":           "3",
    "Vis/SubPixIterations":        "0",
    "Vis/SubPixEps":               "0.02",
    "Vis/RoiRatios":               "0.0 0.0 0.0 0.0",
    "Vis/BundleAdjustment":        "0",

    # ── Frame-to-Map odometry (Odom/Strategy=0) ───────────────────
    "OdometryF2M/MaxSize":                  "1000",
    "OdometryF2M/BundleAdjustment":         "0",
    "OdometryF2M/BundleAdjustmentMaxFrames":"0",
    "OdometryF2M/ScanMaxSize":              "0",
    "OdometryF2M/ScanSubtractRadius":       "0.05",
    "OdometryF2M/ScanSubtractAngle":        "0.0",
    "OdometryF2M/FixedMapPath":             "",

    # ── Frame-to-Frame odometry (Odom/Strategy=1) ─────────────────
    "OdometryF2F/KeyFrameThr":     "0.3",
    "OdometryF2F/ScanKeyFrameThr": "0.9",

    # ── Registration strategy ─────────────────────────────────────
    "Reg/Strategy":                "0",     # 0=Visual  1=ICP  2=Visual+ICP
    "Reg/Force3DoF":               "0",     # MUST be 0 for drone (full 6-DOF)
    "Reg/RepeatOnce":              "1",

    # ── ICP registration (Reg/Strategy=1 or 2) ────────────────────
    "Icp/Strategy":                   "1",
    "Icp/MaxTranslation":             "0.2",
    "Icp/MaxRotation":                "0.78",
    "Icp/MaxCorrespondenceDistance":  "0.05",
    "Icp/VoxelSize":                  "0.05",
    "Icp/DownsamplingStep":           "1",
    "Icp/Iterations":                 "30",
    "Icp/Epsilon":                    "0.001",
    "Icp/CorrespondenceRatio":        "0.1",
    "Icp/PointToPlane":               "1",
    "Icp/PointToPlaneK":              "5",
    "Icp/PointToPlaneRadius":         "0.0",
    "Icp/PointToPlaneGroundNormalsUp":"0.0",
    "Icp/ReciprocalCorrespondences":  "0",
    "Icp/OutlierRatio":               "0.85",
    "Icp/RangeMin":                   "0.0",
    "Icp/RangeMax":                   "0.0",
    "Icp/FiltersEnabled":             "1",
    "Icp/PMMatcherFactor":            "1.0",
    "Icp/PMMatcherMaxDist":           "0.0",
    "Icp/PMMatcherKnn":               "1",
}


SLAM_PARAMS: dict = {

    # ── RTABMap core ──────────────────────────────────────────────
    "Rtabmap/DetectionRate":              "2.0",   # Hz — MUST equal slam.setFreq() == config.VIOSLAM_SLAM_HZ (<= fps)
    "Rtabmap/TimeThr":                    "0.0",
    "Rtabmap/MemoryThr":                  "0",
    "Rtabmap/LoopThr":                    "0.11",
    "Rtabmap/LoopRatio":                  "0.0",
    "Rtabmap/MaxRetrieved":               "2",
    "Rtabmap/ImageDecimation":            "1",
    "Rtabmap/ImagesAlreadyRectified":     "1",
    "Rtabmap/CreateIntermediateNodes":    "0",
    "Rtabmap/StartNewMapOnLoopClosure":   "0",
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
    "RGBD/LinearUpdate":                  "0.1",
    "RGBD/AngularUpdate":                 "0.1",
    "RGBD/LinearSpeedUpdate":             "0.0",
    "RGBD/AngularSpeedUpdate":            "0.0",
    "RGBD/NewMapOdomChangeDistance":      "0.0",
    "RGBD/OptimizeFromGraphEnd":          "0",
    "RGBD/OptimizeMaxError":              "3.0",
    "RGBD/ForceOdom3DoF":                 "0",     # MUST be 0 for drone
    "RGBD/CreateOccupancyGrid":           "1",
    "RGBD/SavedLocalizationIgnored":      "0",
    "RGBD/StartAtOrigin":                 "0",
    "RGBD/MaxLocalRetrieved":             "10",
    "RGBD/MaxOdomCacheSize":              "10",
    "RGBD/LoopClosureReextractFeatures":  "0",
    "RGBD/NeighborLinkRefining":          "0",
    "RGBD/LocalRadius":                   "10.0",
    "RGBD/LocalImmunizationRatio":        "0.25",
    "RGBD/MarkerDetection":               "0",

    # RGBD proximity (space-based loop closure)
    "RGBD/ProximityBySpace":              "1",
    "RGBD/ProximityByTime":               "0",
    "RGBD/ProximityMaxGraphDepth":        "0",
    "RGBD/ProximityMaxPaths":             "3",
    "RGBD/ProximityPathMaxNeighbors":     "10",
    "RGBD/ProximityPathScansMerged":      "0",
    "RGBD/ProximityFilteringRadius":      "1.0",
    "RGBD/ProximityAngle":                "45.0",
    "RGBD/ProximityOdomGuess":            "0",
    "RGBD/ProximityMaxDepth":             "-1",

    # ── Memory management ─────────────────────────────────────────
    "Mem/STMSize":                        "10",
    "Mem/IncrementalMemory":              "1",     # 1=mapping, 0=localisation-only
    "Mem/InitWMWithAllNodes":             "0",
    "Mem/RehearsalSimilarity":            "0.30",
    "Mem/RehearsalIdUpdatedToNewOne":     "0",
    "Mem/ImageKept":                      "1",
    "Mem/BinDataKept":                    "1",
    "Mem/RawDescriptorsKept":             "1",
    "Mem/MapLabelsAdded":                 "1",
    "Mem/SaveDepth16Format":              "0",
    "Mem/NotLinkedNodesKept":             "1",
    "Mem/TransferSortingByWeightId":      "0",
    "Mem/GenerateIds":                    "1",
    "Mem/BadSignaturesIgnored":           "0",
    "Mem/UseOdomGravity":                 "0",
    "Mem/DepthAsMask":                    "1",
    "Mem/ImagePreDecimation":             "1",
    "Mem/ImagePostDecimation":            "1",
    "Mem/IntermediateNodeDataKept":       "1",
    "Mem/LocalizationDataSaved":          "0",
    "Mem/CovOffDiagIgnored":              "1",
    "Mem/GTPoseIgnored":                  "1",
    "Mem/CompressionParallelized":        "1",
    "Mem/LaserScanDownsampleStepSize":    "1",
    "Mem/LaserScanVoxelSize":             "0.0",
    "Mem/LaserScanNormalK":               "0",
    "Mem/LaserScanNormalRadius":          "0.0",

    # ── Keypoints / vocabulary ────────────────────────────────────
    "Kp/DetectorStrategy":                "8",     # MUST match VIO_PARAMS Vis/FeatureType
    "Kp/MaxFeatures":                     "500",
    "Kp/NNStrategy":                      "1",
    "Kp/NndrRatio":                       "0.8",
    "Kp/BadSignRatio":                    "0.5",
    "Kp/WordThr":                         "0",
    "Kp/TfIdfLikelihoodUsed":             "1",
    "Kp/Parallelized":                    "1",
    "Kp/RoiRatios":                       "0.0 0.0 0.0 0.0",
    "Kp/MaxDepth":                        "0.0",
    "Kp/MinDepth":                        "0.0",
    "Kp/SubPixWinSize":                   "3",
    "Kp/SubPixIterations":                "0",
    "Kp/SubPixEps":                       "0.02",
    "Kp/GridRows":                        "1",
    "Kp/GridCols":                        "1",
    "Kp/DictionaryPath":                  "",
    "Kp/NewWordsComparedTogether":        "1",

    # ── Occupancy grid ────────────────────────────────────────────
    "Grid/Sensor":                        "1",     # 0=scan  1=depth  2=both
    "Grid/CellSize":                      "0.05",  # MUST equal config.VIOSLAM_OCC_CELL_SIZE
    "Grid/RangeMin":                      "0.3",
    "Grid/RangeMax":                      "4.0",
    "Grid/NormalsSegmentation":           "1",
    "Grid/MaxGroundAngle":                "45.0",
    "Grid/NormalK":                       "10",
    "Grid/MaxGroundHeight":               "0.1",
    "Grid/MinGroundHeight":               "-0.1",
    "Grid/MaxObstacleHeight":             "2.5",
    "Grid/GroundIsObstacle":              "0",
    "Grid/ClusterRadius":                 "0.1",
    "Grid/MinClusterSize":                "10",
    "Grid/NoiseFilteringRadius":          "0.05",
    "Grid/NoiseFilteringMinNeighbors":    "2",
    "Grid/FootprintLength":               "0.3",
    "Grid/FootprintWidth":                "0.3",
    "Grid/FootprintHeight":               "0.15",
    "Grid/MapFrameProjection":            "0",
    "Grid/3D":                            "1",     # REQUIRED for slam.obstaclePCL
    "Grid/DepthDecimation":               "4",
    "Grid/PreVoxelFiltering":             "1",
    "Grid/FromDepth":                     "1",
    "Grid/FlatObstacleDetected":          "1",
    "Grid/ScanDecimation":                "1",
    "Grid/RayTracing":                    "0",
    "Grid/OccupancyThr":                  "0.5",
    "Grid/ProbHit":                       "0.7",
    "Grid/ProbMiss":                      "0.4",
    "Grid/ClampingThresMin":              "0.1192",
    "Grid/ClampingThresMax":              "0.971",
    "Grid/UpdateError":                   "0.01",

    # ── Pose graph optimiser ──────────────────────────────────────
    "Optimizer/Strategy":                 "1",     # 0=TORO  1=g2o  2=GTSAM  3=Ceres
    "Optimizer/Iterations":               "20",    # g2o converges well within 20; keeps RPi 5 CPU cost low at each detection tick
    "Optimizer/Robust":                   "1",
    "Optimizer/VarianceIgnored":          "0",
    "Optimizer/LandmarksIgnored":         "0",
    "Optimizer/Epsilon":                  "0.0001",
    "Optimizer/GravitySigma":             "0.3",
    "Optimizer/PriorsIgnored":            "1",
    "Optimizer/InvalidMax":               "0",

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
}
