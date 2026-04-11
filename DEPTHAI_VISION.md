# OAK-D Lite Vision & Localization Integration

This document describes the DepthAI v3 / OAK-D Lite integration added to RayeedAI — what hardware is used, how the pipeline works, what the AI can see and do, and how spatial data flows through the system.

---

## Hardware: OAK-D Lite

The [OAK-D Lite](https://docs.luxonis.com/hardware/products/OAK-D%20Lite) is a stereo depth camera that runs computer vision directly on the device.

| Spec | Value |
|---|---|
| RGB camera | 13 MP, up to 4K/30 fps |
| Stereo cameras | Two OV7251 mono sensors, 75 mm baseline |
| Depth resolution | 640 × 400 (hardware cap of OV7251 sensors) |
| Depth range | ~20 cm min — ~10 m practical max |
| On-device VPU | Intel Myriad X — 4 TOPS total, 1.4 TOPS for AI |
| Interface | USB-C (USB 3) |

The Myriad X VPU runs neural networks compiled to `.blob` format entirely on the camera — no cloud, no GPU required on the host.

---

## DepthAI v3 Pipeline (`vision/oak_pipeline.py`)

A single `OakPipeline` instance is built at startup and holds three concurrent processing branches.

### Pipeline architecture

```
                OAK-D Lite hardware
                       │
          ┌────────────┼──────────────┐
          ▼            ▼              ▼
      Camera(RGB)   Camera(L)    Camera(R)
          │            └─────┬────────┘
          │              StereoDepth
          │             (HIGH_DENSITY)
          │                  │
          │         ┌────────┴──────────┐
          │         ▼                   ▼
          │  SpatialLocationCalc    depth queue
          │  (5 sectors, no NN)      (raw frames)
          │         │
          │    sector queue
          │
          ▼
      ImageManip
      (416 × 416)
          │
          ▼
  YoloSpatialDetection     ◄── depth (from StereoDepth)
  (Myriad X VPU, COCO 80)
          │
    detection queue
```

### Key DepthAI v3 API choices

| v2 pattern | v3 pattern used here |
|---|---|
| `XLinkOut` node + `device.getOutputQueue()` | `node.output.createOutputQueue()` directly |
| `ColorCamera` + `MonoCamera` | Unified `Camera.build(socket)` |
| `with dai.Device(pipeline):` | `pipeline.start()` — lifecycle managed internally |

### Three output streams

**1. Raw depth frames** (`stereo.depth` queue, maxSize=1)
- Format: `uint16` ndarray, height × width, values in millimetres
- Invalid pixels: `0` (no disparity) or `65535` (out of range)
- Used by: `vision_depth_snapshot`

**2. SpatialLocationCalculator** (`slc.out` queue, maxSize=4)
- Five horizontal ROI sectors across the middle 40 % of frame height
- Returns median depth per sector in mm (no neural network — runs on CPU)
- Used by: `vision_obstacle_check`

**3. YoloSpatialDetectionNetwork** (`yolo.out` queue, maxSize=4, optional)
- YOLOv6-Nano (416 × 416 input, COCO 80 classes) running on Myriad X
- Returns per-detection: label, confidence, spatial x/y/z in mm
- Blob auto-downloaded at startup via `blobconverter` from Luxonis model zoo
- Disabled gracefully if blob download fails or camera is absent
- Used by: `vision_detect_objects`

---

## Vision Tools (`vision/vision_tool.py`)

Three tools are exposed to the Gemini Live AI model. All are **read-only** — they cannot command the drone. Each runs in `asyncio.to_thread()` so blocking camera reads never stall the audio loop.

### `vision_obstacle_check`

Queries the SpatialLocationCalculator for the five horizontal sectors.

**When the AI calls it:**
```
User: "এগিয়ে যাও"  (Go forward)
AI:   vision_obstacle_check()
```

**Response the AI receives:**
```json
{
  "sectors": {
    "left":         { "distance_m": 3.1, "local_frame": { "forward_m": 2.71, "right_m": -1.51, "down_m": 0.0, "distance_m": 3.1 } },
    "center_left":  { "distance_m": 2.8, "local_frame": { "forward_m": 2.71, "right_m": -0.71, "down_m": 0.0, "distance_m": 2.8 } },
    "center":       { "distance_m": 1.2, "local_frame": { "forward_m": 1.2,  "right_m": 0.0,   "down_m": 0.0, "distance_m": 1.2 } },
    "center_right": { "distance_m": 2.5, "local_frame": { "forward_m": 2.42, "right_m": 0.63,  "down_m": 0.0, "distance_m": 2.5 } }
  },
  "nearest_sector": "center",
  "nearest_distance_m": 1.2,
  "clear": false
}
```

`clear: false` tells the AI there is an obstacle 1.2 m directly ahead. The AI can then decide to slow down, stop, or manoeuvre around it — entirely in natural Bangla reasoning.

---

### `vision_depth_snapshot`

Captures a raw depth frame and performs numpy analysis — no neural network.

**When the AI calls it:**
```
User: "ল্যান্ড করার জায়গা দেখো"  (Look for a landing spot)
AI:   vision_depth_snapshot()
```

**Response the AI receives:**
```json
{
  "frame_shape": [400, 640],
  "nearest_m": 0.8,
  "depth_coverage_pct": 91.3,
  "grid": [
    { "name": "top_left",  "mean_m": 3.2, "min_m": 2.1, "coverage_pct": 88.0 },
    { "name": "top_center","mean_m": 3.0, "min_m": 2.0, "coverage_pct": 94.1 },
    ...
    { "name": "bot_center","mean_m": 2.5, "min_m": 2.4, "coverage_pct": 96.2 }
  ],
  "landing_zone": {
    "safe": true,
    "reason": "flat",
    "std_m": 0.04,
    "coverage_pct": 95.0,
    "mean_m": 2.5,
    "local_frame": { "forward_m": 2.5, "right_m": 0.0, "down_m": 0.0, "distance_m": 2.5 }
  }
}
```

`landing_zone.safe: true` with `std_m: 0.04` tells the AI the ground is flat (4 cm variation) and safe to land on.

---

### `vision_detect_objects`

Runs YOLOv6-Nano on the Myriad X VPU and returns spatial detections.

**When the AI calls it:**
```
User: "সামনে কী আছে?"  (What is in front?)
AI:   vision_detect_objects()
```

**Response the AI receives:**
```json
{
  "count": 2,
  "detections": [
    {
      "label": 0,
      "label_name": "person",
      "confidence": 0.91,
      "x_mm": 45, "y_mm": -12, "z_mm": 2800,
      "local_frame": { "forward_m": 2.8, "right_m": 0.05, "down_m": -0.01, "distance_m": 2.8 }
    },
    {
      "label": 56,
      "label_name": "chair",
      "confidence": 0.74,
      "x_mm": -380, "y_mm": 30, "z_mm": 1500,
      "local_frame": { "forward_m": 1.5, "right_m": -0.38, "down_m": 0.03, "distance_m": 1.55 }
    }
  ]
}
```

The AI sees a person 2.8 m directly ahead and a chair 1.5 m ahead-left. It can reason in Bangla about what to do: announce the person, avoid the chair, or ask the user for instructions.

---

## Localization System (`localization/`)

Raw camera coordinates (mm relative to lens) are meaningless to the AI. The localization layer converts them into spatial language the AI can reason about.

### Coordinate frames

```
Camera frame (DepthAI)       Body FRD frame (AI sees)      World frame (backend only)
 x = right  (mm)              F = forward  (m)              N = north   (m)
 y = down    (mm)      →       R = right    (m)      →       E = east    (m)
 z = forward (mm)              D = down     (m)              D = down    (m)
                                                                  ↓
                                                           GPS lat / lon / alt
```

### Transform chain

```
camera_to_frd(x_mm, y_mm, z_mm, pitch_deg, yaw_deg)
    Axis remap + optional mounting rotation
    → (forward_m, right_m, down_m)

frd_to_ned(f, r, d, heading_deg)
    Rotate by drone compass heading (from TelemetryReader)
    → (north_m, east_m, down_m)

ned_to_global(n, e, d, origin_lat, origin_lon, origin_alt)
    Flat-earth tangent plane approximation
    → (lat, lon, alt_m)
```

### What the AI sees vs. what stays in the backend

| Data | AI sees it? | Where |
|---|---|---|
| `local_frame` (forward_m, right_m, down_m, distance_m) | **Yes** | Added to every detection / sector |
| Raw camera coords (x_mm, y_mm, z_mm) | Yes | Original fields preserved |
| Global GPS (lat, lon, alt_m) | **No** | `Localizer._global_store` deque only |

Global coordinates are stored in a fixed-size deque (`GlobalObservation`, max 200 entries) for future path planning and obstacle mapping — they are never serialised into `ToolResponse.data` and never reach the Gemini model.

### Drone pose (`localization/pose_cache.py`)

`PoseCache` is a thread-safe store that merges two independently-polled data streams:

| Source | Fields | Poll interval |
|---|---|---|
| `TelemetryReader` → `get_telemetry` | `alt_m`, `heading_deg` | 2 s |
| `PositionMonitor` → `get_position_str` | `lat`, `lon` | 5 s |

A `DronePose` is only considered valid if all four fields have been received and the last update was within 10 s. Transforms are skipped silently when the pose is stale.

### Sector angle decomposition

The obstacle-check tool returns only depth (z) per sector. The localizer reconstructs approximate lateral position using each sector's known position within the camera's horizontal FOV (73° default for OAK-D Lite):

```
Sector       Centre x (norm)   Angle from axis
left              0.10              −29.2°
center_left       0.30              −14.6°
center            0.50                0.0°
center_right      0.70              +14.6°
right             0.90              +29.2°

forward_m = depth × cos(angle)
right_m   = depth × sin(angle)
```

---

## Data Flow: Voice Command to Spatial Reasoning

```
User (Bangla voice)
      │
      ▼
Gemini Live API
      │  function call
      ▼
tool_dispatcher.py
      │
      ├─ vision tools? ──► _dispatch_vision()  ──► VisionTool.execute()
      │                                                    │
      │                                              OakPipeline
      │                                         (camera queue reads)
      │                                                    │
      │                                              Localizer.enrich_*()
      │                                              │             │
      │                                        local_frame    GlobalObservation
      │                                        (in response)  (internal deque)
      │
      └─ drone tools? ──► safety check ──► adapter ──► MAVLink / Sim
                                ▲
                          SafetyPolicy
                          (battery, alt,
                           telemetry age)
      │
      ▼
ToolResponse { ok, data: { ..., local_frame: {...} }, state, confidence }
      │
      ▼
Gemini Live API (AI reasons about local_frame values in Bangla)
      │
      ▼
Audio response → speaker
```

---

## Configuration

All vision and localization settings are env-var overridable at runtime.

### Vision pipeline

| Variable | Default | Purpose |
|---|---|---|
| `VISION_ENABLED` | `1` | Set to `0` to disable all vision tools |
| `VISION_FPS` | `15` | Camera frame rate |
| `VISION_DEPTH_MIN_MM` | `200` | Ignore depth closer than this (20 cm) |
| `VISION_DEPTH_MAX_MM` | `8000` | Ignore depth farther than this (8 m) |
| `VISION_BLOB_NAME` | `yolov6n_coco_416x416` | Luxonis model zoo blob name |
| `VISION_BLOB_SHAVES` | `6` | Myriad X shave cores allocated to YOLO |

### Camera mounting calibration

| Variable | Default | Purpose |
|---|---|---|
| `VISION_CAMERA_PITCH_DEG` | `0.0` | Tilt down from drone forward-level (nose-down +) |
| `VISION_CAMERA_YAW_DEG` | `0.0` | Rotation from drone forward axis (clockwise +) |
| `VISION_CAMERA_OFFSET_F_M` | `0.0` | Forward offset of camera from drone centre (m) |
| `VISION_CAMERA_OFFSET_R_M` | `0.0` | Right offset of camera from drone centre (m) |
| `VISION_CAMERA_OFFSET_D_M` | `0.0` | Down offset of camera from drone centre (m) |
| `VISION_CAMERA_HFOV_DEG` | `73.0` | Horizontal field of view (OAK-D Lite RGB default) |

**Example — camera mounted 15° nose-down, 10 cm forward of centre:**
```bash
VISION_CAMERA_PITCH_DEG=15 VISION_CAMERA_OFFSET_F_M=0.1 python app.py
```

---

## Running

```bash
# Install dependencies (includes depthai, blobconverter, numpy, opencv)
pip install -r requirements.txt

# Run with OAK-D Lite attached (sim drone backend)
python app.py

# Run with real drone + OAK-D Lite
DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py

# Disable vision (no camera connected)
VISION_ENABLED=0 python app.py
```

On first launch with vision enabled, `blobconverter` downloads the YOLOv6-Nano blob (~10 MB) from the Luxonis model zoo and caches it locally. Subsequent starts are instant.

---

## Testing

All vision and localization tests run without hardware — no OAK-D Lite or drone required.

```bash
# Vision module tests (37 tests — OakPipeline mocked)
pytest tests/test_vision.py -v

# Localization tests (66 tests — pure math + mock PoseCache)
pytest tests/test_localization.py -v

# Full suite
pytest -v
```

### What is tested

| Test file | Coverage |
|---|---|
| `test_vision.py` | `depth_analyzer` grid stats, landing zone check, `VisionTool` all three handlers with mock pipeline, error paths |
| `test_localization.py` | `camera_to_frd` axis remap + pitch/yaw rotations, `frd_to_ned` all four headings, `ned_to_global` offset math, `sector_to_frd` angular decomposition, `PoseCache` thread safety + staleness, `Localizer` enrichment + global store isolation |

---

## File Reference

```
vision/
  oak_pipeline.py       DepthAI v3 pipeline (Camera, StereoDepth, SLC, YOLO)
  depth_analyzer.py     Numpy depth frame analysis (3×3 grid, flatness check)
  vision_tool.py        Synchronous tool executor — routes dispatcher calls

localization/
  frame_transforms.py   Pure math: camera→FRD→NED→GPS
  pose_cache.py         Thread-safe drone pose (heading, lat/lon, alt)
  localizer.py          Enriches vision results; stores GlobalObservation

telemetry/
  telemetry_reader.py   Polls get_telemetry every 2 s → feeds PoseCache
  position_monitor.py   Polls get_position_str every 5 s → feeds PoseCache

tool_dispatcher.py      Vision tools bypass safety gates → _dispatch_vision()
app.py                  Builds PoseCache → Localizer → VisionTool at startup
config.py               All VISION_* env vars
```
