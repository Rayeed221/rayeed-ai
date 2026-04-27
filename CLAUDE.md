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

The system is a **five-layer pipeline**:

```mermaid
graph LR
    A["🎤 Voice Input"] -->|PCM Audio| B["🤖 Gemini Live API"]
    B -->|Parsed Intent| C["📋 Planner"]
    C -->|Decision: CONTINUE/WAIT/RETRY/REPLAN/ABORT/FAILSAFE| D["⚡ Tool Dispatcher"]
    D -->|Execute Tool| E["🚁 Drone Adapter"]
    E -->|Telemetry| F["📊 State Machine"]
    F -.->|State Update| D
    
    style A fill:#1a1a1a,stroke:#FFD700,stroke-width:3px,color:#FFD700
    style B fill:#1a1a1a,stroke:#00FF00,stroke-width:3px,color:#00FF00
    style C fill:#1a1a1a,stroke:#00FFFF,stroke-width:3px,color:#00FFFF
    style D fill:#1a1a1a,stroke:#FF6B6B,stroke-width:3px,color:#FF6B6B
    style E fill:#1a1a1a,stroke:#9D4EDD,stroke-width:3px,color:#9D4EDD
    style F fill:#1a1a1a,stroke:#00D9FF,stroke-width:3px,color:#00D9FF
```

### Layer Responsibilities

1. **Audio Interface** (`audio/`) — Mic capture → PCM → Gemini; speaker playback. `turn_manager.py` mutes mic while AI is speaking.

2. **LLM Orchestration** (`app.py` + `tools/declarations.py`) — Manages the Gemini Live session, system prompt (Bangla), function declarations, and the resilient receive loop. Session tasks (mic, send, receive, playback) are isolated from background tasks (telemetry, battery, position) so a crash in one doesn't kill the other.

3. **Mission Planning** (`planner.py` + `workflows/`) — Decision engine with 6 outcomes: `CONTINUE`, `WAIT`, `RETRY`, `REPLAN`, `ABORT`, `FAILSAFE`. The planner has **authority to override LLM decisions** for safety. Non-blocking waits allow audio/telemetry to continue during motor spin-up or altitude stabilization.

4. **Safe Execution** (`tool_dispatcher.py` + `safety_policy.py` + `state_machine.py`) — 7-step pipeline: registry check → safety pre-check → execute (10s timeout) → state transition → update monitors → reset retry counter → return `ToolResponse`. Safety gates block operations on low battery, stale telemetry, altitude/speed violations, or exceeded retry counts.

5. **Drone Backend** (`adapters/`) — Swappable via `DRONE_BACKEND` env var. `SimAdapter` (default) simulates all operations in memory. `MAVLinkAdapter` connects to real hardware.

#### Layer Interaction Diagram

```mermaid
graph TB
    subgraph AudioLayer["🎤 Layer 1: Audio Interface"]
        A1["Mic Capture<br/>PCM Stream"]
        A2["Turn Manager<br/>Mute/Unmute"]
        A3["Speaker<br/>Playback"]
    end
    
    subgraph LLMLayer["🤖 Layer 2: LLM Orchestration"]
        L1["Gemini Live<br/>Session"]
        L2["System Prompt<br/>Bangla"]
        L3["Function<br/>Declarations"]
        L4["Receive Loop<br/>Resilient"]
    end
    
    subgraph PlannerLayer["📋 Layer 3: Mission Planning"]
        P1["Decision Engine<br/>6 Outcomes"]
        P2["Workflows<br/>Replan Logic"]
        P3["Non-blocking<br/>Waits"]
    end
    
    subgraph DispatcherLayer["⚡ Layer 4: Safe Execution"]
        D1["Tool Registry"]
        D2["Safety Policy"]
        D3["State Machine"]
        D4["7-Step Pipeline"]
    end
    
    subgraph AdapterLayer["🚁 Layer 5: Drone Backend"]
        DR1["SimAdapter<br/>Memory Sim"]
        DR2["MAVLinkAdapter<br/>Hardware"]
    end
    
    A1 --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    D4 --> DR1
    D4 --> DR2
    DR1 --> A2
    DR2 --> A2
    A2 --> A3
    
    style AudioLayer fill:#1a1a1a,stroke:#FFD700,stroke-width:2px,color:#FFD700
    style LLMLayer fill:#1a1a1a,stroke:#00FF00,stroke-width:2px,color:#00FF00
    style PlannerLayer fill:#1a1a1a,stroke:#00FFFF,stroke-width:2px,color:#00FFFF
    style DispatcherLayer fill:#1a1a1a,stroke:#FF6B6B,stroke-width:2px,color:#FF6B6B
    style AdapterLayer fill:#1a1a1a,stroke:#9D4EDD,stroke-width:2px,color:#9D4EDD
```

### Key Files

| File | Role |
|---|---|
| `app.py` | Entry point; `DroneAI` class; Gemini Live session management |
| `state_machine.py` | Mission states (IDLE→CONNECTED→ARMED→TAKEOFF→ENROUTE→HOVER→LANDING→RTL→FAILSAFE) and legal transition graph |
| `tool_dispatcher.py` | Central 7-step execution pipeline for all drone commands |
| `safety_policy.py` | Pre-execution gates: battery, telemetry freshness, altitude ceiling, speed, retry limits |
| `planner.py` | Decision engine; overrides LLM `next_action`; schedules non-blocking waits |
| `tool_registry.py` | Metadata for 25+ tools: description, arg schema, permission level, allowed states |
| `schemas.py` | `ToolResponse` envelope (ok, tool, state, data, error, next_action, wait, confidence, timestamp) |
| `config.py` | All thresholds and env vars (API key, audio rates, backend, safety limits) |

### Tool Execution Flow

Every drone command goes through `tool_dispatcher.py`:

```mermaid
graph TD
    A["📥 Incoming Tool Request"] --> B["🔍 Step 1: Registry Check<br/>Tool exists?"]
    B -->|Not Found| Z["❌ Return Error"]
    B -->|Found| C["⚠️ Step 2: Safety Pre-Check<br/>Battery ≥15%?<br/>Telemetry Fresh &lt;5s?<br/>Altitude &lt;120m?<br/>Speed &lt;15 m/s?<br/>Retries &lt;3?"]
    C -->|Unsafe| Z
    C -->|Safe| D["⚡ Step 3: Execute<br/>Adapter.execute 10s timeout"]
    D -->|Timeout/Error| E{"Retryable?"}
    E -->|Yes| F["🔄 Retry<br/>Increment Counter"]
    F --> D
    E -->|No| Z
    D -->|Success| G["🔗 Step 4: State Transition<br/>Update state_machine"]
    G --> H["📊 Step 5: Update Monitors<br/>Safety monitors"]
    H --> I["🔄 Step 6: Reset Retry<br/>Clear retry counter"]
    I --> J["📦 Step 7: Return<br/>ToolResponse OK"]
    J --> K["✅ Response to Planner"]
    Z --> K
    
    style A fill:#1a1a1a,stroke:#FFD700,stroke-width:2px,color:#FFD700
    style B fill:#1a1a1a,stroke:#00FFFF,stroke-width:2px,color:#00FFFF
    style C fill:#1a1a1a,stroke:#FF6B6B,stroke-width:2px,color:#FF6B6B
    style D fill:#1a1a1a,stroke:#9D4EDD,stroke-width:2px,color:#9D4EDD
    style E fill:#1a1a1a,stroke:#FFB347,stroke-width:2px,color:#FFB347
    style F fill:#1a1a1a,stroke:#FF1493,stroke-width:2px,color:#FF1493
    style G fill:#1a1a1a,stroke:#00FF00,stroke-width:2px,color:#00FF00
    style H fill:#1a1a1a,stroke:#00D9FF,stroke-width:2px,color:#00D9FF
    style I fill:#1a1a1a,stroke:#00FF00,stroke-width:2px,color:#00FF00
    style J fill:#1a1a1a,stroke:#00FF00,stroke-width:2px,color:#00FF00
    style K fill:#1a1a1a,stroke:#FFD700,stroke-width:2px,color:#FFD700
    style Z fill:#1a1a1a,stroke:#FF0000,stroke-width:3px,color:#FF0000
```

1. Registry check (tool exists?)
2. Safety pre-check (battery ≥15%, telemetry fresh <5s, altitude <120m, speed <15 m/s, retries <3)
3. Execute via adapter (10s timeout)
4. State machine transition
5. Update safety monitors
6. Reset retry counter on success
7. Return normalized `ToolResponse`

### State Machine Rules

- `force_failsafe()` is always allowed from any state
- Tools declare which states they are valid in (e.g., `takeoff` only in `ARMED`)
- `is_airborne()` covers TAKEOFF, ENROUTE, HOVER, LANDING, RTL

#### Mission State Flow

```mermaid
stateDiagram-v2
    [*] --> IDLE
    IDLE --> CONNECTED: connect_drone()
    CONNECTED --> ARMED: arm_drone()
    ARMED --> TAKEOFF: takeoff()
    TAKEOFF --> ENROUTE: goto_position()
    ENROUTE --> HOVER: hover_at_position()
    HOVER --> ENROUTE: goto_position()
    HOVER --> LANDING: land()
    LANDING --> IDLE: motor_stop()
    
    ARMED --> RTL: return_to_launch()
    ENROUTE --> RTL: return_to_launch()
    HOVER --> RTL: return_to_launch()
    
    IDLE --> FAILSAFE: force_failsafe()
    CONNECTED --> FAILSAFE: force_failsafe()
    ARMED --> FAILSAFE: force_failsafe()
    TAKEOFF --> FAILSAFE: force_failsafe()
    ENROUTE --> FAILSAFE: force_failsafe()
    HOVER --> FAILSAFE: force_failsafe()
    RTL --> FAILSAFE: force_failsafe()
    LANDING --> FAILSAFE: force_failsafe()
    
    RTL --> IDLE: landing_complete()
    FAILSAFE --> IDLE: disarm_drone()
    
    style IDLE fill:#1a1a1a,stroke:#FFD700,stroke-width:2px,color:#FFD700
    style CONNECTED fill:#1a1a1a,stroke:#00FF00,stroke-width:2px,color:#00FF00
    style ARMED fill:#1a1a1a,stroke:#00FFFF,stroke-width:2px,color:#00FFFF
    style TAKEOFF fill:#1a1a1a,stroke:#FF6B6B,stroke-width:2px,color:#FF6B6B
    style ENROUTE fill:#1a1a1a,stroke:#9D4EDD,stroke-width:2px,color:#9D4EDD
    style HOVER fill:#1a1a1a,stroke:#00D9FF,stroke-width:2px,color:#00D9FF
    style LANDING fill:#1a1a1a,stroke:#FFB347,stroke-width:2px,color:#FFB347
    style RTL fill:#1a1a1a,stroke:#FF1493,stroke-width:2px,color:#FF1493
    style FAILSAFE fill:#1a1a1a,stroke:#FF0000,stroke-width:3px,color:#FF0000
```

### Backend Abstraction

Both adapters implement the same interface from `adapters/base_adapter.py`. Switching between sim and MAVLink requires only an env var change — no code changes.

```mermaid
graph LR
    A["⚡ Tool Dispatcher<br/>asyncio.to_thread"] --> B["🔧 Base Adapter<br/>Interface"]
    B --> C{"DRONE_BACKEND<br/>env var"}
    C -->|sim| D["🖥️ SimAdapter<br/>Memory Simulation<br/>Default"]
    C -->|mavlink| E["🚁 MAVLinkAdapter<br/>Real Hardware<br/>pymavlink"]
    D --> F["18 Handler Methods<br/>execute"]
    E --> G["18 Handler Methods<br/>execute"]
    F --> H["ToolResponse<br/>Normalized"]
    G --> H
    H --> I["Back to Dispatcher"]
    
    style A fill:#1a1a1a,stroke:#FFD700,stroke-width:2px,color:#FFD700
    style B fill:#1a1a1a,stroke:#00FF00,stroke-width:2px,color:#00FF00
    style C fill:#1a1a1a,stroke:#FFB347,stroke-width:2px,color:#FFB347
    style D fill:#1a1a1a,stroke:#00FFFF,stroke-width:2px,color:#00FFFF
    style E fill:#1a1a1a,stroke:#FF6B6B,stroke-width:2px,color:#FF6B6B
    style F fill:#1a1a1a,stroke:#00FFFF,stroke-width:2px,color:#00FFFF
    style G fill:#1a1a1a,stroke:#FF6B6B,stroke-width:2px,color:#FF6B6B
    style H fill:#1a1a1a,stroke:#9D4EDD,stroke-width:2px,color:#9D4EDD
    style I fill:#1a1a1a,stroke:#FFD700,stroke-width:2px,color:#FFD700
```

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
|---|---|
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
