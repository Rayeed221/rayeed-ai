# RTAB-Map Parameters Reference for DepthAI v3

## Quick Start

To use parameters with DepthAI v3 RTABMapSLAM node:

```python
slam = p.create(dai.node.RTABMapSLAM)
params = {
    "RGBD/Enabled": "true",
    "Grid/3D": "true",
    # Add more parameters...
}
slam.setParams(params)
```

---

## Core SLAM Parameters (`Rtabmap/`)

### Detection & Processing

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Rtabmap/DetectionRate` | Float | 1.0 | Detection rate in Hz. Higher = more loop closures but more CPU. Drone: 2-3 Hz recommended |
| `Rtabmap/TimeThr` | Int | 0 | Max time for map update (ms). 0 = infinity. Set to 700 for real-time constraint |
| `Rtabmap/MemoryThr` | Int | 0 | Max nodes in Working Memory before transfer to Long-Term. 0 = unlimited. Drone: 200-300 |
| `Rtabmap/LoopThr` | Float | 0.11 | Loop closure threshold (0-1). Lower = stricter. Range: 0.05-0.2 |
| `Rtabmap/LoopRatio` | Float | 0.0 | Hypothesis must exceed this ratio of last value |
| `Rtabmap/SaveWMState` | Bool | false | Save working memory state to database |

### Loop Closure

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Rtabmap/LoopCounterIdThr` | Int | 3 | Minimum IDs between loop closure candidates |
| `Rtabmap/LoopClosureReextractFeatures` | Bool | false | Re-extract features for loop closure validation |

---

## RGB-D SLAM Parameters (`RGBD/`)

### Core Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `RGBD/Enabled` | Bool | true | Enable RGB-D SLAM mode. **MUST BE TRUE** |
| `RGBD/CreateOccupancyGrid` | Bool | false | Create 2D occupancy grid from point clouds |

### Movement Thresholds

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `RGBD/LinearUpdate` | Float | 0.1 | Minimum linear movement (meters) to add new node. Outdoor: 0.2, Indoor: 0.05 |
| `RGBD/AngularUpdate` | Float | 0.1 | Minimum angular movement (radians) to add new node. ~6 degrees. Outdoor: 0.15 |

### Optimization

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `RGBD/OptimizeFromGraphEnd` | Bool | false | Optimize from last node (true) or first node (false) |
| `RGBD/OptimizeMaxError` | Float | 3.0 | Reject loop closures if optimization error exceeds this |

### Proximity & Loop Closure

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `RGBD/LocalRadius` | Float | 10.0 | Local map radius in meters. Drone/outdoor: 10-15m |
| `RGBD/MaxLoopClosureDistance` | Float | 0.0 | Max distance for loop closure (0 = no limit). Outdoor: 10-20m |
| `RGBD/ProximityBySpace` | Bool | true | Enable detection of locations near in space |
| `RGBD/ProximityMaxGraphDepth` | Int | 50 | Max graph depth for proximity hypotheses |
| `RGBD/ProximityPathMaxNeighbors` | Int | 10 | Max neighbors in proximity path |
| `RGBD/LocalLoopDetectionSpace` | Bool | true | Enable local loop detection by space |
| `RGBD/LocalLoopDetectionTime` | Bool | false | Enable local loop detection by time |
| `RGBD/NeighborLinkRefining` | Bool | false | Refine transformation of neighbor links |

---

## Visual Processing Parameters (`Vis/`)

### Feature Extraction

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Vis/MaxFeatures` | Int | 1000 | Max features per image. Fast: 200-500, Accurate: 800-1000 |
| `Vis/MinInliers` | Int | 20 | Minimum inliers required for valid transformation |
| `Vis/InlierDistance` | Float | 0.1 | Max distance (meters) for feature correspondence inliers |

### Estimation Method

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Vis/EstimationType` | Int | 0 | Motion estimation: 0=3D-3D, 1=PnP, 2=Epipolar Geometry |
| `Vis/Iterations` | Int | 300 | Max iterations for transform computation |
| `Vis/CorrespondenceType` | Int | 0 | 0=Features Matching, 1=Optical Flow |

---

## Keypoint Detection (`Kp/`)

### General Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Kp/MaxFeatures` | Int | 500 | Maximum keypoints to extract from image |
| `Kp/DetectorStrategy` | Int | 6 | Feature detector: 0=SURF, 6=GFTT, 8=ORB, 9=FAST, 11=KAZE |
| `Kp/NndrRatio` | Float | 0.8 | Nearest neighbor distance ratio (Lowe's ratio test) |

### Detector Strategy Options

- **0**: SURF - Good all-around, patented
- **6**: GFTT (Good Features To Track) - Fast, reliable
- **8**: ORB - Fast, free, good for outdoor
- **9**: FAST - Very fast corner detection
- **11**: KAZE - Scale-space detection
- **12**: BRISK - Binary descriptor
- **14**: SuperPoint - Deep learning based (if available)

---

## Feature Detector Specific Parameters

### GFTT (Good Features To Track)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `GFTT/QualityLevel` | Float | 0.001 | Minimal accepted quality of corners |
| `GFTT/MinDistance` | Float | 7.0 | Minimum distance between detected features |
| `GFTT/BlockSize` | Int | 3 | Size of averaging block for corner detection |
| `GFTT/UseHarrisDetector` | Bool | false | Use Harris corner detector vs Shi-Tomasi |

### ORB (Oriented FAST and Rotated BRIEF)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ORB/ScaleFactor` | Float | 1.2 | Pyramid decimation ratio (>1) |
| `ORB/NLevels` | Int | 8 | Number of pyramid levels |
| `ORB/EdgeThreshold` | Int | 19 | Border size where features are not detected |
| `ORB/WTA_K` | Int | 2 | Number of points for oriented BRIEF descriptor |
| `ORB/PatchSize` | Int | 31 | Size of patch used for BRIEF descriptor |

### FAST (Features from Accelerated Segment Test)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `FAST/Threshold` | Int | 20 | Threshold on difference between intensity |
| `FAST/NonmaxSuppression` | Bool | true | Apply non-maximum suppression |
| `FAST/MinThreshold` | Int | 7 | Min threshold for adaptive FAST |
| `FAST/MaxThreshold` | Int | 200 | Max threshold for adaptive FAST |

---

## Grid/Occupancy Parameters (`Grid/`)

### Basic Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Grid/3D` | Bool | true | Create 3D occupancy grid vs 2D projection |
| `Grid/CellSize` | Float | 0.05 | Grid cell size in meters. Fast: 0.1, Accurate: 0.02-0.05 |
| `Grid/RangeMax` | Float | 5.0 | Maximum range for obstacle detection (meters) |
| `Grid/ClusterRadius` | Float | 0.1 | Cluster radius for filtering (meters) |

### Environment Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Grid/GroundIsObstacle` | Bool | false | Treat ground surface as obstacle |
| `Grid/MaxObstacleHeight` | Float | 0.0 | Max obstacle height (meters). 0 = no limit. Outdoor: 2-3m |
| `Grid/MinGroundHeight` | Float | 0.0 | Minimum ground height (meters) |
| `Grid/NormalsSegmentation` | Bool | true | Use normal-based segmentation |
| `Grid/FromDepth` | Bool | true | Create grid from depth image |

### Global Grid

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `GridGlobal/MinSize` | Float | 20.0 | Minimum global grid size (meters) |

---

## Optimizer Parameters (`Optimizer/`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Optimizer/Strategy` | Int | 1 | Backend: 0=TORO, 1=g2o, 2=GTSAM, 3=Ceres. g2o recommended |
| `Optimizer/Iterations` | Int | 20 | Number of optimization iterations. Range: 10-50 |
| `Optimizer/Epsilon` | Float | 0.0 | Convergence threshold |
| `Optimizer/Robust` | Bool | false | Use robust graph optimization (Vertigo) |
| `Optimizer/GravitySigma` | Float | 0.0 | Gravity constraint sigma for IMU integration. Drone: 0.3 |

---

## Memory Management (`Mem/`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Mem/IncrementalMemory` | Bool | true | SLAM mode (true) vs Localization mode (false) |
| `Mem/ImageKept` | Bool | false | Keep raw images in RAM |
| `Mem/STMSize` | Int | 10 | Short-term memory size (number of nodes) |
| `Mem/RehearsalSimilarity` | Float | 0.6 | Threshold for rehearsal node matching |
| `Mem/BadSignaturesIgnored` | Bool | false | Ignore bad signatures during matching |
| `Mem/ImageCompressionFormat` | String | ".jpg" | Image compression format (.jpg or .png) |
| `Mem/DepthCompressionFormat` | String | "" | Depth compression format (.png or .rvl) |

---

## Database Parameters (`DbSqlite3/`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `DbSqlite3/InMemory` | Bool | false | Use in-memory database vs disk |
| `DbSqlite3/CacheSize` | Int | 10000 | SQLite cache size (KB) |
| `DbSqlite3/JournalMode` | String | "WAL" | Journal mode: DELETE, WAL, MEMORY |
| `DbSqlite3/Synchronous` | Int | 0 | Synchronous mode: 0=OFF, 1=NORMAL, 2=FULL |

---

## Recommended Configurations

### 🚁 Drone / Fast Movement

```python
params = {
    "Rtabmap/DetectionRate": "3.0",
    "Rtabmap/MemoryThr": "200",
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.2",
    "RGBD/AngularUpdate": "0.15",
    "RGBD/CreateOccupancyGrid": "true",
    "RGBD/LocalRadius": "15.0",
    "Vis/MaxFeatures": "800",
    "Vis/MinInliers": "15",
    "Kp/DetectorStrategy": "8",  # ORB
    "Grid/3D": "true",
    "Grid/CellSize": "0.1",
    "Grid/RangeMax": "20.0",
    "Optimizer/Strategy": "1",
}
```

### 🎯 High Accuracy / Slow Movement

```python
params = {
    "Rtabmap/DetectionRate": "1.0",
    "Rtabmap/MemoryThr": "0",
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.05",
    "RGBD/AngularUpdate": "0.05",
    "RGBD/CreateOccupancyGrid": "true",
    "RGBD/ProximityBySpace": "true",
    "Vis/MaxFeatures": "1000",
    "Vis/MinInliers": "20",
    "Kp/DetectorStrategy": "6",  # GFTT
    "GFTT/QualityLevel": "0.001",
    "Grid/3D": "true",
    "Grid/CellSize": "0.02",
    "Optimizer/Iterations": "30",
}
```

### ⚡ Performance / Real-time

```python
params = {
    "Rtabmap/DetectionRate": "2.0",
    "Rtabmap/MemoryThr": "300",
    "RGBD/Enabled": "true",
    "RGBD/LinearUpdate": "0.1",
    "RGBD/AngularUpdate": "0.1",
    "RGBD/CreateOccupancyGrid": "true",
    "Vis/MaxFeatures": "500",
    "Vis/MinInliers": "15",
    "Kp/DetectorStrategy": "8",  # ORB - fastest
    "Grid/3D": "true",
    "Grid/CellSize": "0.05",
    "Optimizer/Strategy": "1",
    "Optimizer/Iterations": "20",
}
```

### 🔄 Loop Closure Focused

```python
params = {
    "Rtabmap/DetectionRate": "2.0",
    "Rtabmap/LoopThr": "0.11",
    "RGBD/Enabled": "true",
    "RGBD/CreateOccupancyGrid": "true",
    "RGBD/ProximityBySpace": "true",
    "RGBD/ProximityMaxGraphDepth": "50",
    "RGBD/LocalLoopDetectionSpace": "true",
    "Vis/MaxFeatures": "1000",
    "Vis/MinInliers": "20",
    "Mem/RehearsalSimilarity": "0.6",
    "Grid/3D": "true",
}
```

---

## Parameter Value Types

- **Bool**: Use string `"true"` or `"false"`
- **Int**: Use string representation, e.g., `"20"`
- **Float**: Use string representation, e.g., `"0.1"`
- **String**: Use quoted string, e.g., `".jpg"`

---

## Tuning Tips

1. **Start with defaults** - Don't change everything at once
2. **Adjust movement thresholds first** - `RGBD/LinearUpdate` and `RGBD/AngularUpdate` have biggest impact
3. **Balance features vs speed** - More features = better accuracy but slower
4. **Match detector to environment** - ORB for outdoor, GFTT for indoor
5. **Monitor memory usage** - Set `Rtabmap/MemoryThr` to prevent RAM overflow
6. **Use loop closure for long sequences** - Helps correct drift
7. **Grid resolution affects performance** - Coarser grids (0.1m) are faster

---

## Resources

- [RTAB-Map Official Documentation](http://introlab.github.io/rtabmap/)
- [Parameters.h Source](https://github.com/introlab/rtabmap/blob/master/corelib/include/rtabmap/core/Parameters.h)
- [DepthAI v3 Documentation](https://docs.luxonis.com/software-v3/depthai/)
- [ROS RTAB-Map Tutorials](https://wiki.ros.org/rtabmap_ros/Tutorials/Advanced%20Parameter%20Tuning)
