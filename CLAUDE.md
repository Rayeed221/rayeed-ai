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

# Run all tests
pytest

# Run a single test file
pytest tests/test_state_machine.py -v

# Run tests with async support
pytest tests/test_failures.py -v
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

2. **LLM Orchestration** (`app.py` + `tools/declarations.py`) — Manages the Gemini Live session, system prompt (Bangla), function declarations, and the resilient receive loop. Session tasks (mic, send, receive, playback) are isolated from background tasks (telemetry, battery, position, avoidance) so a crash in one doesn't kill the other.

3. **Mission Planning** (`planner.py` + `workflows/`) — Decision engine with 6 outcomes: `CONTINUE`, `WAIT`, `RETRY`, `REPLAN`, `ABORT`, `FAILSAFE`. The planner has **authority to override LLM decisions** for safety. Phase 1b inserts an avoidance gate: returns `WAIT` while DroNet is actively steering around an obstacle, escalates to `REPLAN` if stuck > 10 s continuously.

4. **Safe Execution** (`tool_dispatcher.py` + `safety_policy.py` + `state_machine.py`) — 7-step pipeline: registry check → safety pre-check → execute (10s timeout) → state transition → update monitors → reset retry counter → return `ToolResponse`. Safety gates block operations on low battery, stale telemetry, altitude/speed violations, exceeded retry counts, **or active DroNet avoidance** (`goto_position` / `set_speed` are gated when `collision_prob ≥ AVOIDANCE_COLLISION_THR`).

5. **Drone Backend** (`adapters/`) — Swappable via `DRONE_BACKEND` env var. `SimAdapter` (default) simulates all operations in memory. `MAVLinkAdapter` connects to real hardware.

6. **Avoidance Layer** (`vision/avoidance/dronet_runner.py`) — `DroNetRunner` runs PULP-DroNet v3 on the OAK-D Lite at ~20 Hz as an asyncio background task. Publishes `AvoidanceState` (thread-safe); sends `SET_POSITION_TARGET_LOCAL_NED` velocity commands directly over MAVLink. Non-fatal if depthai or OAK-D are absent.

### Key Files

| File | Role |
| --- | --- |
| `app.py` | Entry point; `DroneAI` class; Gemini Live session + background task group |
| `state_machine.py` | Mission states (IDLE→CONNECTED→ARMED→TAKEOFF→ENROUTE→HOVER→LANDING→RTL→FAILSAFE) and legal transition graph |
| `tool_dispatcher.py` | Central 7-step execution pipeline; enriches `vision_obstacle_check` with live DroNet state |
| `safety_policy.py` | Pre-execution gates: battery, telemetry, altitude, speed, retry limits, **avoidance** |
| `planner.py` | Decision engine; Phase 1b avoidance gate; overrides LLM `next_action`; non-blocking waits |
| `tool_registry.py` | Metadata for 25+ tools: description, arg schema, permission level, allowed states |
| `schemas.py` | `ToolResponse` envelope (ok, tool, state, data, error, next_action, wait, confidence, timestamp) |
| `config.py` | All thresholds and env vars (API keys, audio rates, backend, safety limits, avoidance thresholds) |
| `vision/avoidance/dronet_runner.py` | `DroNetRunner` + `AvoidanceState`; autonomous 20 Hz avoidance loop |
| `vision/avoidance/run_dronet_oak.py` | Standalone DroNet CLI (unchanged by integration) |

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

`DroNetRunner` runs as a fourth background task alongside `TelemetryReader`, `BatteryMonitor`, and `PositionMonitor`. `SafetyPolicy` holds a direct reference to the runner and reads `AvoidanceState` on-demand — no polling relay task.

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

## MAVLink Adapter Implementation

The stub lives at `adapters/mavlink_adapter.py`. All 18 `_handle_*()` methods exist but return `{"error": "MAVLink not yet wired..."}`. The `SimAdapter` at `adapters/sim_adapter.py` is the reference implementation — match its structure exactly.

### Dependency

`pymavlink` is **not in `requirements.txt`** — add it before implementing:

```bash
pip install pymavlink
# then add "pymavlink" to requirements.txt
```

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

Mirror `tests/test_tools.py` — it covers all 18 handlers for `SimAdapter` and is the template for MAVLink tests. Adapter tests are **not async** (the `asyncio.to_thread` wrapping is the dispatcher's job):

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

## Testing

Framework: `pytest` + `pytest-asyncio`. All test files are in `tests/`. Each major subsystem has its own test file covering normal paths, error/retry paths, and state transitions.
