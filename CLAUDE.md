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

# Run with real drone via MAVLink (default URI: tcp:127.0.0.1:5762)
DRONE_BACKEND=mavlink MAVLINK_URI=udp:192.168.1.10:14550 python app.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_workflows.py -v

# Run one specific test
pytest tests/test_failures.py::test_decide_failsafe_on_battery_critical_error -v
```

## Architecture

The system is a **five-layer pipeline**:

```
Voice Input → Gemini Live API → Planner → Tool Dispatcher → Drone Adapter
```

### Layer Responsibilities

1. **Audio Interface** (`audio/`) — Mic capture → PCM → Gemini; speaker playback. `turn_manager.py` mutes mic while AI is speaking.

2. **LLM Orchestration** (`app.py` + `tools/declarations.py`) — Manages the Gemini Live session, system prompt (Bangla), function declarations, and the resilient receive loop. Session tasks (mic, send, receive, playback) are isolated from background tasks (telemetry, battery, position) so a crash in one doesn't kill the other.

3. **Mission Planning** (`planner.py` + `workflows/`) — Decision engine with 6 outcomes: `CONTINUE`, `WAIT`, `RETRY`, `REPLAN`, `ABORT`, `FAILSAFE`. The planner has **authority to override LLM decisions** for safety. Non-blocking waits allow audio/telemetry to continue during motor spin-up or altitude stabilization.

4. **Safe Execution** (`tool_dispatcher.py` + `safety_policy.py` + `state_machine.py`) — 7-step pipeline: registry check → safety pre-check → execute (10s timeout) → state transition → update monitors → reset retry counter → return `ToolResponse`. Safety gates block operations on low battery, stale telemetry, altitude/speed violations, or exceeded retry counts.

5. **Drone Backend** (`adapters/`) — Swappable via `DRONE_BACKEND` env var. `SimAdapter` (default) simulates all operations in memory. `MAVLinkAdapter` connects to real hardware via `pymavlink`.

### Background subsystems

- `telemetry/` — `TelemetryReader`, `BatteryMonitor`, `PositionMonitor` run as independent asyncio tasks. A crash in any of them is isolated from the session tasks (see `DroneAI.run()` in `app.py` for the two-group task split).
- `memory/` — `MissionMemory` persists the last tool + mission state to `memory_store/mission_state.json` after every tool call; `EnvironmentMemory` stores named waypoints / obstacles / no-fly zones in `memory_store/environment.json`.

### Key Files

| File | Role |
|---|---|
| `app.py` | Entry point; `DroneAI` class; Gemini Live session management |
| `state_machine.py` | Mission states (IDLE→CONNECTED→ARMED→TAKEOFF→ENROUTE→HOVER→LANDING→RTL→FAILSAFE) and legal transition graph |
| `tool_dispatcher.py` | Central 7-step execution pipeline for all drone commands |
| `safety_policy.py` | Pre-execution gates: battery, telemetry freshness, altitude ceiling, speed, retry limits |
| `planner.py` | Decision engine; overrides LLM `next_action`; `execute_step()` helper drives workflows |
| `tool_registry.py` | Metadata for 18 tools: description, arg schema, permission level, allowed states |
| `schemas.py` | `ToolResponse` envelope (ok, tool, state, data, error, next_action, wait, confidence, timestamp) |
| `config.py` | All thresholds and env vars (API key, audio rates, backend, safety limits) |

### Tool Execution Flow

Every drone command goes through `tool_dispatcher.py`:
1. Registry check (tool exists?)
2. Safety pre-check (battery ≥15%, telemetry fresh <5s, altitude <120m, speed <15 m/s, retries <3)
3. Execute via adapter (10s timeout, wrapped in `asyncio.to_thread` so adapters can be synchronous)
4. State machine transition
5. Update safety monitors (`update_telemetry_timestamp`, `update_battery`, `update_altitude` are triggered by specific tool names — see `tool_dispatcher.py:128-133`)
6. Reset retry counter on success
7. Return normalized `ToolResponse`

### State Machine Rules

- `force_failsafe()` is always allowed from any state
- Tools declare which states they are valid in via `allowed_states` in `tool_registry.py` (e.g., `takeoff` only in `ARMED`); `None` means any state
- `is_airborne()` covers TAKEOFF, ENROUTE, HOVER, RTL (note: LANDING is **not** airborne — see `state_machine.py:67-71`)

### Workflows (`workflows/`)

Code-driven flight sequences (`startup`, `takeoff`, `navigation`, `inspection`, `landing`, `return_home`, `emergency`). Each exports an `async def run_<name>(dispatcher, sm, safety, planner, ...)` coroutine.

**Primitive**: every non-emergency workflow step goes through `planner.execute_step(tool_name, args)`, which centralizes dispatch + wait + retry + failsafe + abort handling. A typical step is a single line:

```python
if not await planner.execute_step("arm_drone", {}):
    return False
```

The `emergency` workflow is the exception — it calls `dispatcher.dispatch()` directly (wrapped in `_try()` with a short timeout) so it never blocks or raises, even when the link is dead.

### Backend Abstraction

Both adapters implement the same interface from `adapters/base_adapter.py`. Switching between sim and MAVLink requires only an env var change — no code changes.

Adapter handlers (`_handle_<tool_name>`) are **synchronous** — the dispatcher wraps `adapter.execute()` in `asyncio.to_thread()`, so blocking pymavlink calls (`wait_heartbeat`, `recv_match`, `time.sleep`) are safe inside handlers.

### MAVLink adapter return-shape contract

`safety_policy.py`, `planner.py`, and `tool_dispatcher.py` read specific fields from adapter return dicts — field names must match exactly. The contract is visible in `adapters/sim_adapter.py` (reference) and mirrored in `adapters/mavlink_adapter.py`.

**Critical**: `safety_policy.update_battery()` is fed from `get_battery` results where the dispatcher reads the key `level_percent` (not `percent` or `battery_pct`). See `tool_dispatcher.py:131`.

On any failure, handlers return `{"error": "<description>"}` — the dispatcher treats this as a retryable error and increments the retry counter.

## Configuration (`config.py`)

Key env vars:
- `GEMINI_API_KEY` — Gemini API key (a default is hardcoded for dev; override in env for anything real)
- `DRONE_BACKEND` — `"sim"` (default) or `"mavlink"`
- `MAVLINK_URI` — MAVLink connection string (default: `tcp:127.0.0.1:5762`)

Safety thresholds (all configurable):
- Battery critical: 15% → failsafe; Battery low: 25% → planner `REPLAN` toward RTH
- Altitude ceiling: 120m
- Max speed: 15 m/s
- Telemetry stale: 5s → wait; 10s → emergency failsafe
- Max retries: 3

## Testing

Framework: `pytest` + `pytest-asyncio`. Tests live in `tests/`:

| File | Covers |
|---|---|
| `test_state_machine.py` | Legal/illegal transitions, force_failsafe, is_airborne |
| `test_schemas.py` | `ToolResponse`, `WaitInstruction`, `ErrorSchema` serialization |
| `test_tools.py` | All 18 `_handle_*` shapes for `SimAdapter` — template for adapter tests |
| `test_failures.py` | Planner decision table + all `SafetyPolicy` checks |
| `test_workflows.py` | End-to-end workflow coroutines with a mocked dispatcher |

Workflow tests inject an `AsyncMock` dispatcher and use `ToolResponse.success()` / `ToolResponse.failure()` helpers — see `tests/test_workflows.py:13-17`. Adapter tests are **not async** (the `asyncio.to_thread` wrapping is the dispatcher's job).
