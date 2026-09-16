# Latency — where it goes, what changed

This note maps the tiered drone-agent grammar (reflex / navigation / mission,
with a compact symbolic vocabulary instead of natural-language reasoning) onto
the actual hot paths in this codebase, and records what was changed.

The organising idea from that design is that **reasoning belongs at the mission
tier, not in the loop that answers every step**. Almost all the latency found
here was some version of the same mistake: a deliberative or blocking mechanism
sitting inside a path that a lookup could have answered.

---

## The two paths that matter

```text
VOICE PATH   (what the user waits for)
  mic → Gemini Live → tool_call
      → dispatcher (safety gate → adapter → state machine)
      → planner.decide()
      → send_tool_response  → Gemini speaks

REFLEX PATH  (what the airframe waits for)
  OAK-D → DroNetRunner → MAVLink velocity command   ~20 Hz, no LLM
```

The reflex path was already correct — `DroNetRunner` never touches the LLM or
the tool pipeline. Everything below is about the voice path, where four separate
mechanisms were adding delay to every single step of a mission.

---

## Findings

### 1. Blocking MAVLink reads that also stole each other's messages — the big one

`mavutil.recv_match(type=X, blocking=True, timeout=5.0)` **discards every
message that is not X** while it waits. Four independent consumers shared one
connection — `TelemetryReader` (2 s), `PositionMonitor` (5 s), `BatteryMonitor`
(10 s), and every LLM tool call — each inside its own `asyncio.to_thread`
worker. They consumed each other's messages, so a read that should have been
free drifted toward its 5 s timeout. pymavlink connections are not thread-safe
either, so this was a correctness hazard as much as a latency one.

`get_telemetry` was the worst case: a blocking wait for `GLOBAL_POSITION_INT`
*plus* a second blocking wait for `VFR_HUD`.

**Fixed** — `adapters/mavlink_cache.py`. One reader thread owns the socket,
drains it continuously, and stores the latest message per type. Handlers read
that cache in O(1). This is the `STATE` primitive of the grammar: a value that
is always current, not a round trip that has to be paid for.

- `get_telemetry` / `get_position_str` / `get_battery` / `get_current_state`
  are now cache reads (~microseconds, measured at <0.5 ms for 1000 reads).
- `MAVLINK_CACHE_MAX_AGE_SEC` (default 0.5 s) bounds staleness: past that the
  handler waits for a fresh message, so a dead link still surfaces as an error
  rather than a stale reading.
- `COMMAND_ACK` is correlated by command id *and* a send timestamp, so a late
  ACK for one command can no longer satisfy the wait for another.
- Sends are serialised by a lock.
- The reader thread filters out HEARTBEATs from other systems — our own
  avoidance layer emits GCS heartbeats, and caching one would corrupt mode
  detection.

### 2. `set_mode` confirmed itself against a 1 Hz stream

`goto_position`, `takeoff`, `land` and `return_to_launch` all route through
`set_mode`, which sent `DO_SET_MODE` and then blocked for a `HEARTBEAT` showing
the new mode — **even when the vehicle was already in that mode**. After
takeoff the vehicle is already in GUIDED, so every `goto_position` paid up to a
full heartbeat period for a no-op.

**Fixed** — `set_mode` returns immediately when the cached heartbeat already
shows the requested mode, and otherwise confirms by polling the cache.

### 3. Every `wait_altitude` / `wait_arrival` was guaranteed to fail

`TOOL_TIMEOUT_SEC = 10.0` applied to every tool, but the adapter waits up to
60 s for altitude and 120 s for arrival. So the dispatcher cut them off at 10 s,
returned `next_action="retry"`, burned a retry counter and an extra LLM round
trip — while the orphaned thread kept running and kept consuming MAVLink
messages. Every takeoff paid this.

**Fixed** — `tool_dispatcher.timeout_for()` gives each tool a budget that
matches what it is actually waiting for (`wait_time` derives its budget from
its own argument). The wait loops themselves now poll the cache at 20 Hz
instead of doing a 2 s blocking read plus a 0.2 s sleep per iteration, so they
also detect arrival up to ~2.2 s sooner.

### 4. A local LLM inside every voice round trip

`planner.decide()` runs between the dispatcher and the tool result the Live
model is waiting for. Its oracle gate was:

```python
return tool_name in HIGH_VALUE_TOOLS or not ok or airborne
```

`airborne` means **every tool call in flight** triggered a qwen3:0.6b
generation with `think=True` and `num_predict=96`. The workflows did it again
per step — a four-step takeoff meant four serial local generations.

Worse, three things made that cost pure waste:

- `ORACLE_TIMEOUT` was stored and **never enforced**. A slow or stalled Ollama
  blocked the voice round trip for as long as it took.
- `_from_dict` was defined on `ThinkingOracle`, but both parse paths called
  `ThinkingDecision._from_dict`. `AttributeError` is not in either call site's
  `except` clause, so it escaped to `deliberate()`'s catch-all — meaning **every
  successful parse was discarded and the rule fallback was used every time**.
  The oracle paid full latency and never once affected a decision.
- The thinking block was ~90% of the generated tokens, for what is a six-way
  classification.

**Fixed** — `planner.py` now runs three tiers:

| Tier | What it is | Cost |
| --- | --- | --- |
| 1. `reflex()` | deterministic table; every hard safety gate and every nominal outcome | **1.1 µs** (measured) |
| 2. oracle | consulted only on `ReflexVerdict.UNKNOWN` — a *repeated* failure of a flight-critical tool | bounded by `ORACLE_DEADLINE_SEC` (1.5 s) |
| 3. rule fallback | same thresholds as `safety_policy.py` | microseconds |

The decision *contract* is unchanged — `reflex()` evaluates the same gates in
the same order the old Phase 1/Phase 3 did, and `tests/test_drone/test_failures.py`
asserts each one. Only *when the model is consulted* changed.

Also in this tier:

- a real deadline (`asyncio.wait_for`), so the oracle can never hold up a tool
  result;
- a single-flight guard — a second caller falls straight through to the rules
  rather than queueing behind the first on a one-model backend;
- `_from_dict` moved onto `ThinkingDecision`, so oracle output is finally parsed;
- `think=False`, `num_predict=32`, a newline stop token, and `keep_alive` so the
  model stays resident;
- the compact output grammar `DECISION | reason` (JSON still accepted), because
  output tokens are the oracle's latency;
- `prewarm()` at startup, so the first in-flight decision is not a cold load.

`planner.decision_stats()` reports `reflex_rate` — the fraction of decisions
answered with no model in the loop. It is logged at shutdown.

### 5. Tool results carried fields the model never reads

Every tool result was sent as the full `asdict()`: an epoch float `timestamp`,
plus `error`/`next_action`/`wait`/`confidence` even when null or at default. The
Live model re-tokenises all of it before it can speak, and it compounds because
the session keeps the exchange in context.

**Fixed** — `ToolResponse.to_llm()` drops null/default fields and the timestamp,
and passes `data` through untouched. **44% smaller** across representative
calls (measured). `ToolResponse.sentence()` adds the tiny-sentence log form
(`OK takeoff | hover | next=wait_altitude`) used for mission memory.

### 6. Audio output buffering

`sd.OutputStream` was constructed without a latency hint, so PortAudio used its
`'high'` default (~100 ms+ of output buffering on a Pi) on every AI reply.
Now `AUDIO_OUTPUT_LATENCY`, default `low`. Set it back to `high` if the board
underruns and crackles — this is the one change here with a real hardware
trade-off.

---

## Config knobs added

```bash
MAVLINK_CACHE_MAX_AGE_SEC=0.5    # staleness bound on cached reads
MAVLINK_ACK_TIMEOUT_SEC=3.0      # was a hardcoded 10 s
MAVLINK_MODE_CONFIRM_SEC=3.0     # was a hardcoded 5 s
MAVLINK_WAIT_ALTITUDE_SEC=60.0   # adapter deadline; dispatcher budget follows it
MAVLINK_WAIT_ARRIVAL_SEC=120.0

ORACLE_ENABLED=1                 # 0 = reflex + rules only, no model at all
ORACLE_DEADLINE_SEC=1.5          # hard budget, now actually enforced
ORACLE_THINK=0                   # 1 to restore chain-of-thought for debugging
ORACLE_NUM_PREDICT=32
ORACLE_KEEP_ALIVE=30m
ORACLE_PREWARM=1

AUDIO_OUTPUT_LATENCY=low         # high | low | float seconds
COMPACT_TOOL_RESPONSE=1          # 0 to send the full ToolResponse dict
```

Rebuild the oracle model after pulling, so it emits the compact grammar:

```bash
ollama create droneoracle -f thinking_oracle.Modelfile
```

(The parser accepts both the compact line and the old JSON, so an un-rebuilt
model keeps working.)

---

## Not done — the biggest remaining win

**Compound workflow tools.** The LLM is handed 21 flat primitives, so
"১০ মিটারে ওঠো" costs four Gemini Live round trips: `arm_drone` →
`takeoff` → `wait_altitude` → `get_telemetry`. The sequences already exist as
`workflows/takeoff.py` and `workflows/navigation.py` — they are simply not
exposed as tools. Exposing `run_takeoff(altitude)` as a single declaration
would collapse those four round trips into one and let the sequence run at
local speed under the planner's authority. That is the article's Level 3
(mission) vs Level 1 (reflex) separation, and it is worth more than everything
above combined.

It is not in this change because it alters mission semantics: a long-running
workflow either blocks the tool response for its whole duration, or returns
immediately and leaves the LLM unable to tell the user when the takeoff
finished. Resolving that needs a way to push workflow completion back into the
Live session, which is a design decision rather than a tuning one.

**Related, smaller:** `wait_altitude` / `wait_arrival` are still blocking tools.
The `WaitInstruction` / `planner.schedule_wait()` machinery for non-blocking
waits already exists and is used for the short hints, but the long waits do not
go through it. Routing them through the planner would free the voice path
during a climb.

---

## Verifying

```bash
pytest tests/test_drone -q          # 308 passing
```

New coverage: `test_mavlink_cache.py` (blackboard, ACK correlation, concurrent
readers), `test_mavlink_adapter_fastpath.py` (cached reads, `set_mode` no-op,
disconnected handlers return errors rather than raising),
`test_dispatch_timeouts.py` (per-tool budgets), plus reflex-tier and compact
payload tests in `test_failures.py` and `test_schemas.py`.

In flight, watch two log lines:

```text
[MAVLINK] Cache primed: {'running': True, 'errors': 0, 'ages_sec': {...}}
[PLANNER] Decision tiers: {'reflex_hits': N, 'escalations': M, 'reflex_rate': 0.9x, ...}
```

A `reflex_rate` near 1.0 means the model is out of the hot path, which is the
whole point.
