# RayeedAI — রাইদ-এআই

Voice-controlled autonomous drone assistant. Speak in **Bangla**; the AI flies the drone.

Built on Python + Google Gemini Live API + MAVLink. Runs on Android (Termux), Linux, and macOS.

---

## Quick start

```bash
pip install -r requirements.txt

# Simulator (default)
python app.py

# Real drone via MAVLink
DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py
```

The drone auto-connects at startup — no tool call needed.

---

## Architecture — five-layer pipeline

```
Voice → Gemini Live → Planner → Dispatcher → Adapter → Drone
```

| Layer | Directory | Responsibility |
|---|---|---|
| 1. Audio | `audio/` | Mic capture, playback, turn muting |
| 2. LLM | `app.py` + `tools/declarations.py` | Gemini Live session, function declarations |
| 3. Planning | `planner.py` + `workflows/` | Decision engine + code-driven flight sequences |
| 4. Safe execution | `tool_dispatcher.py` + `safety_policy.py` + `state_machine.py` | Gates, retries, state transitions |
| 5. Backend | `adapters/` | SimAdapter (default) or MAVLinkAdapter |

Background tasks (`telemetry/`, `memory/`) run isolated from the session — a crash in one does not kill audio.

---

## LLM tool surface — 7 intent verbs

The LLM does **not** see primitives (arm, set_mode, wait_*). It works at mission-intent level:

| Tool | Purpose |
|---|---|
| `get_status` | Unified snapshot — mode, armed, altitude, battery, GPS, EKF, home |
| `takeoff(altitude)` | GUIDED + arm + takeoff + wait-altitude, composed internally |
| `goto_position(lat, lon, alt, speed_ms?, yaw_deg?)` | Auto-takes off first if grounded |
| `land` | Land + disarm |
| `return_to_launch` | Fly home + land + disarm |
| `hold_position(seconds, yaw_deg?)` | Hold for inspection |
| `emergency_stop(reason?)` | Failsafe: RTL → land → disarm |

Internal primitives live in `tool_registry.py` (18 tools) and are composed by workflows in `workflows/`.

---

## Safety gates (`safety_policy.py`)

Every tool is checked before execution:

- **Battery** — `<15%` → failsafe; `<25%` → planner replans toward RTH
- **Altitude ceiling** — `120 m`
- **Max speed** — `15 m/s`
- **Telemetry freshness** — stale `>5 s` → wait; `>10 s` → emergency
- **EKF health** — blocks `takeoff`/`arm_drone` when attitude / horizontal-velocity / absolute-position flags are not all valid
- **Retries** — max 3 per tool

---

## State machine

```
IDLE → CONNECTED → ARMED → TAKEOFF → ENROUTE ⇄ HOVER → LANDING → IDLE
                                        ↓
                                       RTL → LANDING
                   FAILSAFE  (reachable from any state)
```

`force_failsafe()` overrides the transition graph. Tools declare `allowed_states` in `tool_registry.py`.

---

## Backends

Swap via env var — no code change.

| Backend | Connection |
|---|---|
| `sim` (default) | In-memory `SimAdapter` |
| `mavlink` | `MAVLinkAdapter` via pymavlink, 50 Hz stream reader, default `tcp:127.0.0.1:5762` |

The MAVLink adapter runs a single daemon thread that routes all messages into a thread-safe snapshot, so every consumer (telemetry reader, battery monitor, safety policy) reads the same cached state with no socket contention.

---

## Configuration (`config.py`)

| Env var | Default | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | dev key | Gemini API |
| `DRONE_BACKEND` | `sim` | `sim` or `mavlink` |
| `MAVLINK_URI` | `tcp:127.0.0.1:5762` | MAVLink endpoint |

Safety thresholds (battery %, altitude ceiling, speed, stale windows, retry cap) are all in `config.py`.

---

## Testing

```bash
pytest                                  # run all
pytest tests/test_workflows.py -v       # one file
pytest tests/test_failures.py::test_decide_failsafe_on_battery_critical_error -v
```

| Test file | Covers |
|---|---|
| `test_state_machine.py` | Legal/illegal transitions |
| `test_schemas.py` | `ToolResponse` / `WaitInstruction` / `ErrorSchema` |
| `test_tools.py` | All 18 adapter handlers + snapshot shape |
| `test_failures.py` | Planner decisions + safety checks |
| `test_workflows.py` | End-to-end workflow coroutines + intent registry |

---

## Project layout

```
app.py                   # entry point, Gemini Live session
planner.py               # 6-outcome decision engine
safety_policy.py         # pre-execution gates
state_machine.py         # mission states + transitions
tool_dispatcher.py       # 7-step execution pipeline
tool_registry.py         # primitive metadata
schemas.py               # ToolResponse envelope
config.py                # env + thresholds

adapters/    sim_adapter.py, mavlink_adapter.py, base_adapter.py
audio/       mic_capture.py, playback.py, turn_manager.py
memory/      mission_memory.py, environment_memory.py
telemetry/   telemetry_reader.py, battery_monitor.py, position_monitor.py
tools/       declarations.py (LLM-facing function schemas)
workflows/   startup, takeoff, navigation, inspection, landing,
             return_home, emergency, registry
tests/       pytest suite
```
