# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**DroneAI (RayeedAI — রাইদ-এআই)** is a voice-controlled autonomous drone assistant using Python and the Google Gemini Live API. It accepts natural language voice commands in **Bangla** and translates them into drone flight operations. The system runs entirely async and supports a simulated drone backend (default) or real drone hardware via MAVLink.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run with simulated drone (default)
python app.py

# Run with real drone via MAVLink
DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py

# Run headless / CI (no OAK-D, no SLAM pipeline)
VISION_ENABLED=0 VIOSLAM_ENABLED=0 python app.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_drone/test_state_machine.py -v

# Run tests with async support
pytest tests/test_drone/test_failures.py -v
```

## Architecture

The system has **two independent command layers** on top of a five-layer pipeline:

```text
                    LAYER 1 — Mission Layer
Voice Input → Gemini Live API → Planner → Tool Dispatcher → Drone Adapter
                                                  ↓ (on-demand, seconds apart)
                                              MAVLink / FC

                    LAYER 2 — Avoidance Layer (autonomous, no LLM)
                    DroNetRunner (OAK-D Lite + PULP-DroNet v3)
                                                  ↓ (~20 Hz velocity commands)
                                              MAVLink / FC
```

In ArduPilot GUIDED mode, velocity commands are ephemeral — they override the position setpoint for one cycle only, so both layers coexist without conflict.

### Layer Responsibilities

1. **Audio Interface** (`audio/`) — Mic capture → PCM → Gemini; speaker playback. `turn_manager.py` mutes mic while AI is speaking.

2. **LLM Orchestration** (`app.py` + `tools/declarations.py`) — Manages the Gemini Live session, system prompt (Bangla), function declarations, and the resilient receive loop. Session tasks (mic, send, receive, playback) are isolated from the **five** background tasks (telemetry, battery, position, avoidance, VIO/SLAM) so a crash in one doesn't kill the other.

3. **Mission Planning** (`planner.py` + `workflows/`) — Decision engine with 6 outcomes: `CONTINUE`, `WAIT`, `RETRY`, `REPLAN`, `ABORT`, `FAILSAFE`. The planner has **authority to override LLM decisions** for safety. Phase 1b inserts an avoidance gate: returns `WAIT` while DroNet is actively steering around an obstacle, escalates to `REPLAN` if stuck > 10 s continuously.

4. **Safe Execution** (`tool_dispatcher.py` + `safety_policy.py` + `state_machine.py`) — 7-step pipeline: registry check → safety pre-check → execute (10s timeout) → state transition → update monitors → reset retry counter → return `ToolResponse`. Safety gates block operations on low battery, stale telemetry, altitude/speed violations, exceeded retry counts, **or active DroNet avoidance** (`goto_position` / `set_speed` are gated when `collision_prob ≥ AVOIDANCE_COLLISION_THR`).

5. **Drone Backend** (`adapters/`) — Swappable via `DRONE_BACKEND` env var. `SimAdapter` (default) simulates all operations in memory. `MAVLinkAdapter` connects to real hardware.

6. **Avoidance Layer** (`vision/avoidance/dronet_runner.py`) — `DroNetRunner` runs PULP-DroNet v3 on the OAK-D Lite at ~20 Hz as an asyncio background task. Publishes `AvoidanceState` (thread-safe); sends `SET_POSITION_TARGET_LOCAL_NED` velocity commands directly over MAVLink. Non-fatal if depthai or OAK-D are absent.

7. **VIO/SLAM Layer** (`localization/vio_slam/vio_slam_runner.py`) — `VIOSLAMRunner` is the **fifth** background task (default `VIOSLAM_ENABLED=1`). Owns its own DepthAI v3 RTAB-Map VIO+SLAM pipeline; publishes `VIOPose` into `PoseCache` and a `LiveOccupancyGrid` that `safety_policy.py` reads for a SLAM-proximity gate. Non-fatal if depthai/OAK-D are absent. See "VIO and SLAM Integration" below — this is now **production-wired**, no longer exploration-only.

8. **Memory Layer** (`memory/`) — Two JSON-backed stores (`memory_store/`, gitignored): `MissionMemory` persists mission state + an event log (`mission_log.jsonl`) for crash recovery; `EnvironmentMemory` persists spatial knowledge (named waypoints, obstacle markers, no-fly zones) across sessions. Both are constructed in `app.py`.

### Key Files

| File | Role |
| --- | --- |
| `app.py` | Entry point; `DroneAI` class; Gemini Live session + background task group |
| `state_machine.py` | Mission states (IDLE→CONNECTED→ARMED→TAKEOFF→ENROUTE→HOVER→LANDING→RTL→FAILSAFE) and legal transition graph |
| `tool_dispatcher.py` | Central 7-step execution pipeline; enriches `vision_obstacle_check` with live DroNet state |
| `safety_policy.py` | Pre-execution gates: battery, telemetry, altitude, speed, retry limits, **DroNet avoidance**, **SLAM proximity** |
| `planner.py` | Decision engine; Phase 1b avoidance gate; overrides LLM `next_action`; non-blocking waits |
| `tool_registry.py` | Metadata for 25+ tools: description, arg schema, permission level, allowed states |
| `schemas.py` | `ToolResponse` envelope; also `MissionEvent` used by `memory/` |
| `config.py` | All thresholds and env vars (API keys, audio rates, backend, safety limits, avoidance + VIO/SLAM thresholds) |
| `vision/avoidance/dronet_runner.py` | `DroNetRunner` + `AvoidanceState`; autonomous 20 Hz avoidance loop |
| `vision/avoidance/run_dronet_oak.py` | Standalone DroNet CLI (unchanged by integration) |
| `localization/vio_slam/vio_slam_runner.py` | `VIOSLAMRunner`; production VIO+SLAM background task; publishes `VIOPose` + `LiveOccupancyGrid` |
| `memory/mission_memory.py` | Crash-recovery state + JSONL event log (`memory_store/`) |
| `memory/environment_memory.py` | Persistent waypoints / obstacles / no-fly zones |

### Tool Execution Flow

Every drone command goes through `tool_dispatcher.py`:

1. Registry check (tool exists?)
2. Safety pre-check (battery ≥15%, telemetry fresh <5s, altitude <120m, speed <15 m/s, **avoidance inactive**, retries <3)
3. Execute via adapter (10s timeout)
4. State machine transition
5. Update safety monitors
6. Reset retry counter on success
7. Return normalized `ToolResponse`

### Avoidance Integration

`DroNetRunner` runs as the fourth background task alongside `TelemetryReader`, `BatteryMonitor`, and `PositionMonitor` (with `VIOSLAMRunner` as the fifth). `SafetyPolicy` holds a direct reference to the runner and reads `AvoidanceState` on-demand — no polling relay task.

Key constants in `config.py`:

- `DRONET_MODEL_PATH` — path to MyriadX blob (default: `vision/avoidance/dronet_tiny_openvino_2022.1_5shave.blob`)
- `AVOIDANCE_COLLISION_THR` — collision probability gate threshold (default: `0.7`)
- `AVOIDANCE_STALE_SEC` — seconds before avoidance state is considered stale (default: `0.5`)

The LLM never calls avoidance directly. It observes obstacle state through the existing `vision_obstacle_check` tool, whose response now includes a `"dronet"` key with live `collision_prob`, `depth_mm`, `steering`, and `active` fields.

### State Machine Rules

- `force_failsafe()` is always allowed from any state
- Tools declare which states they are valid in (e.g., `takeoff` only in `ARMED`)
- `is_airborne()` covers TAKEOFF, ENROUTE, HOVER, LANDING, RTL

### Backend Abstraction

Both adapters implement the same interface from `adapters/base_adapter.py`. Switching between sim and MAVLink requires only an env var change — no code changes.

## VIO and SLAM Integration

### Current State (Production-Wired)

VIO/SLAM is **now integrated** as the package `localization/vio_slam/` and runs as a background task in `app.py` when `VIOSLAM_ENABLED=1` (the default). The production runner (`VIOSLAMRunner`) mirrors `vision/avoidance/dronet_runner.py` 1:1: lazy `import depthai` inside `run()`, all blocking DepthAI calls wrapped in `asyncio.to_thread()`, thread-safe state behind one lock, cooperative cancel via `CancelledError`.

**Production package (`localization/vio_slam/`):**

| File | Role |
| --- | --- |
| `vio_slam_runner.py` | `VIOSLAMRunner` background task; owns the DepthAI pipeline; publishes pose + grid |
| `slam_state.py` | `VIOPose`, `SLAMSnapshot` thread-safe dataclasses |
| `occupancy_grid.py` | `LiveOccupancyGrid` — 3D obstacle grid with decay; queried by `safety_policy.check_slam_proximity()` |
| `rtabmap_params.py` | `VIO_PARAMS` / `SLAM_PARAMS` dicts (see knob docs below) |

> **Hardware constraint:** the OAK-D Lite's Myriad X cannot host RTABMapSLAM + SpatialLocationCalculator + YOLO at once. Enable **only one** of `{VISION_ENABLED, VIOSLAM_ENABLED}` per OAK-D unit. `rtabmap_params.py` forces the C numeric locale at import so a comma-decimal system locale can't corrupt the string-valued params.

**SLAM proximity gate:** `safety_policy.py` holds a `VIOSLAMRunner` reference (`set_vioslam_runner()`) and blocks `goto_position` / `set_speed` when the occupancy grid shows an obstacle within `VIOSLAM_PROXIMITY_THR_M` along the forward vector (pose must be fresher than `VIOSLAM_STALE_SEC`).

### Existing Localization System (Production)

### Existing Localization System (Production)

Three files handle coordinate enrichment today, replacing GPS-only reasoning with camera-space awareness:

- **`localization/frame_transforms.py`** — Pure math: `camera_to_frd()` → `frd_to_ned()` → `ned_to_global()`. Flat-earth approximation. No SLAM.
- **`localization/pose_cache.py`** — Thread-safe `PoseCache`: merges heading/altitude from `TelemetryReader` and lat/lon from `PositionMonitor`. Staleness check (invalid if any field missing or >10s old).
- **`localization/localizer.py`** — Enriches vision detections with `local_frame` coordinates. Stores `GlobalObservation` deque for AI reasoning. Handles stale pose gracefully.

### VIO/SLAM Pipeline Topology

Built in `localization/vio_slam/vio_slam_runner.py` with the **DepthAI v3 API**:

```text
CAM_B + CAM_C (stereo)
  → StereoDepth (depth aligned to CAM_B)
      ├── rectifiedLeft → FeatureTracker (HARRIS, 1000 features)
      │       ├── passthroughInputImage → RTABMapVIO.rect
      │       └── outputFeatures → RTABMapVIO.features
      ├── depth → RTABMapVIO.depth
IMU (ACCELEROMETER_RAW + GYROSCOPE_RAW @ 200 Hz) → RTABMapVIO.imu
      │
RTABMapVIO.transform → RTABMapSLAM.odom
RTABMapVIO.passthroughRect → RTABMapSLAM.rect
RTABMapVIO.passthroughDepth → RTABMapSLAM.depth
```

`RTABMapVIO` and `RTABMapSLAM` are host (`ThreadedHostNode`) nodes — they run on
the RPi 5 CPU; the rest runs on the OAK-D Lite's Myriad X.

### VIO Parameters (Key Knobs)

`RTABMapVIO.setParams()` — all string-valued:

- `Odom/Strategy`: `"0"` (F2M, frame-to-map) — default and best for drones
- `Vis/FeatureType`: `"8"` (GFTT+ORB) — fast, runs on Myriad X; matches `Kp/DetectorStrategy`
- `Vis/MaxFeatures` / `Vis/MinInliers`: `"600"` / `"15"` — lower = faster, less accurate
- `Vis/MaxDepth` / `Vis/MinDepth`: `"4.0"` / `"0.3"` — match to `Icp/RangeMin`/`Max` and `Grid/RangeMax`
- `Reg/Force3DoF`: **must be `"0"`** for drones (full 6-DOF); `"1"` is for ground robots only
- `OdometryF2M/MaxSize`: `"1000"` — local 3D map size; higher = more accurate, more RAM

### SLAM Parameters (Key Knobs)

`RTABMapSLAM.setParams()` — all string-valued:

- `slam.setFreq(2.0)` — SLAM node runs at 2 Hz (VIO runs at camera fps)
- `Rtabmap/DetectionRate`: **must equal** `slam.setFreq()` (both `2.0`) and be **≤ `VIOSLAM_FPS`** — frames only arrive at camera fps, so a higher SLAM rate cannot be honored
- `Mem/IncrementalMemory`: `"1"` (mapping) vs `"0"` (localization-only mode)
- `slam.setLoadDatabaseOnStart(True)` — for relocalization into a previously saved map
- `slam.setSaveDatabasePeriod(60.0)` — auto-save interval in seconds
- `Grid/3D`: `"1"` — 3D voxel grid; required for obstacle point cloud (`slam.obstaclePCL`)
- `Grid/CellSize`: `"0.05"` — 5 cm resolution; matches `LiveOccupancyGrid` default
- `Optimizer/Strategy`: `"1"` (g2o) — pose graph optimizer; `"2"` is GTSAM
- `Kp/DetectorStrategy` **must match** `Vis/FeatureType` (both `"8"` for GFTT+ORB)

### Pipeline Outputs (wired into the main system)

**Outputs consumed from the VIO+SLAM pipeline:**

| Queue | Data | Use |
| --- | --- | --- |
| `vio.transform` | 6-DOF pose (translation + quaternion) | Published as `VIOPose` into `PoseCache` |
| `slam.transform` | Loop-closure-corrected pose | Primary `PoseCache` source when available |
| `slam.obstaclePCL` | 3D obstacle point cloud | Fed to `LiveOccupancyGrid` for the SLAM proximity gate |
| `slam.groundPCL` | Ground point cloud | Landing zone detection |

**Frame convention for VIO poses:** VIO transform is in the camera's starting frame (camera Z = forward, X = right, Y = down). Use `localization/frame_transforms.py` to convert to NED/GPS before writing to `PoseCache`.

### map.db

`map.db` (repo root, gitignored) is the RTAB-Map database. The runner writes it
via `VIOSLAM_DB_PATH` and auto-saves every 60 s; set `VIOSLAM_LOAD_DB=1` to load
a saved map on start for relocalization.

## MAVLink Adapter Implementation

The stub lives at `adapters/mavlink_adapter.py`. All 18 `_handle_*()` methods exist but return `{"error": "MAVLink not yet wired..."}`. The `SimAdapter` at `adapters/sim_adapter.py` is the reference implementation — match its structure exactly.

### Execution Model

All handler methods must remain **synchronous**. The dispatcher wraps every `adapter.execute()` call with `asyncio.to_thread()`, so blocking pymavlink calls (e.g., `wait_heartbeat()`, `recv_match()`) are safe inside handlers.

### Connection Pattern

```python
from pymavlink import mavutil
self._conn = mavutil.mavlink_connection(self._connection_string)
self._conn.wait_heartbeat()
```

### Required Handler Return Shapes

The dispatcher, planner, and safety policy read specific fields from these dicts — field names must match exactly:

| Handler | Must Return |
| --- | --- |
| `_handle_connect_drone` | `{"status": "connected", "connection_string": str}` |
| `_handle_get_telemetry` | `{"altitude": float, "airspeed": float, "groundspeed": float, "heading": float}` |
| `_handle_get_position_str` | `{"position": "Lat: X, Lon: X, Alt: X"}` |
| `_handle_get_battery` | `{"voltage": float, "current": float, "level_percent": float}` |
| `_handle_get_current_state` | `{"mode": str, "armed": bool, "system_status": str}` |
| `_handle_get_distance_to_str` | `{"distance_str": str, "bearing": float}` |
| `_handle_set_mode` | `{"status": "ok", "mode": str}` |
| `_handle_arm_drone` | `{"status": "armed"}` |
| `_handle_disarm_drone` | `{"status": "disarmed"}` |
| `_handle_takeoff` | `{"status": "taking_off", "target_altitude": float}` |
| `_handle_land` | `{"status": "landing"}` |
| `_handle_return_to_launch` | `{"status": "returning_to_launch"}` |
| `_handle_goto_position` | `{"status": "moving", "target": {"lat": float, "lon": float, "alt": float}}` |
| `_handle_set_yaw` | `{"status": "ok", "yaw_deg": float}` |
| `_handle_set_speed` | `{"status": "ok", "speed_ms": float}` |
| `_handle_wait_altitude` | `{"status": "altitude_reached", "altitude": float}` |
| `_handle_wait_arrival` | `{"status": "arrived"}` |
| `_handle_wait_time` | `{"status": "done", "waited_seconds": float}` |

On any failure, return `{"error": "<description>"}` — the dispatcher treats this as a retryable error and increments the retry counter.

> **Critical**: `safety_policy.py` reads `level_percent` (not `percent` or `battery_pct`) from the `get_battery` response to enforce battery thresholds. This field name is non-negotiable.

### Testing the Adapter

Mirror `tests/test_drone/test_tools.py` — it covers all 18 handlers for `SimAdapter` and is the template for MAVLink tests. Adapter tests are **not async** (the `asyncio.to_thread` wrapping is the dispatcher's job):

```python
@pytest.fixture
def mav():
    adapter = MAVLinkAdapter("udp:127.0.0.1:14550")
    # mock self._conn if testing without hardware
    return adapter

def test_get_battery_shape(mav):
    result = mav.execute("get_battery", {})
    assert "level_percent" in result  # must match — safety_policy reads this key
    assert "voltage" in result
```

## Configuration (`config.py`)

Key env vars:

- `GEMINI_API_KEY` — Gemini API key
- `DRONE_BACKEND` — `"sim"` (default) or `"mavlink"`
- `MAVLINK_URI` — MAVLink connection string (default: `udp:127.0.0.1:14550`)

Safety thresholds (all configurable):

- Battery critical: 15% → failsafe; Battery low: 25% → warn
- Altitude ceiling: 120m
- Max speed: 15 m/s
- Telemetry stale: 5s → wait; 10s → emergency failsafe
- Max retries: 3

Vision & avoidance:

- `VISION_ENABLED` — default `0`; set `1` to enable YOLO vision tools (mutually exclusive with `VIOSLAM_ENABLED` per OAK-D)
- `DRONET_MODEL_PATH` — path to MyriadX blob
- `AVOIDANCE_COLLISION_THR` (`0.7`) / `AVOIDANCE_STALE_SEC` (`0.5`) — DroNet gate thresholds

VIO/SLAM (all read in `config.py`, default **enabled**):

- `VIOSLAM_ENABLED` — default `1`; owns the OAK-D VIO+SLAM background task
- `VIOSLAM_DB_PATH` (`map.db`) / `VIOSLAM_LOAD_DB` (`0`) — RTAB-Map DB path and relocalization-load flag
- `VIOSLAM_FPS` (`10`) / `VIOSLAM_SLAM_HZ` (`2.0`) — camera/VIO-loop rate and SLAM node rate. Tuned for a **USB 2.0 link on RPi 5**: at 640×400 the host RTABMap nodes pull ~768 KB/frame (depth + rectified) over USB, so ~7.7 MB/s at 10 fps stays well under the USB2 ceiling; SLAM runs on the RPi 5 CPU, hence 2 Hz. Invariant: `VIOSLAM_SLAM_HZ == SLAM_PARAMS["Rtabmap/DetectionRate"] ≤ VIOSLAM_FPS`.
- `VIOSLAM_FORCE_USB2` — default `1`; pins the OAK-D to USB 2.0 High-Speed (`dai.Device(dai.UsbSpeed.HIGH)` → `dai.Pipeline(device)`). Set `0` to auto-negotiate on a USB3 bench setup.
- `VIOSLAM_OCC_CELL_SIZE` (`0.05`) — **must equal** `SLAM_PARAMS["Grid/CellSize"]`
- `VIOSLAM_PROXIMITY_THR_M` (`1.5`) / `VIOSLAM_STALE_SEC` (`0.5`) — SLAM proximity gate distance and pose-freshness bound

## Testing

Framework: `pytest` + `pytest-asyncio`. Most test files are in `tests/test_drone/` — each major subsystem has its own file covering normal paths, error/retry paths, and state transitions (including `test_vio_slam_runner.py`, `test_occupancy_grid.py`, `test_localization.py`). `tests/test_depthai/test_oak_pipeline_reconnect.py` covers the OAK-D pipeline reconnect logic using a faked `depthai` module (no hardware needed).
