"""
Planner decisions (Decision 4 — Planner authority overrides LLM for safety):

  continue  → next tool in workflow
  wait      → non-blocking wait; audio + telemetry keep running
  retry     → increment retry count, re-dispatch same tool
  replan    → re-evaluate current workflow route
  abort     → stop mission gracefully
  failsafe  → force emergency workflow immediately

Non-blocking wait (Decision 5B): planner.schedule_wait() sets a timer.
Callers poll planner.is_waiting() before advancing. Audio and
telemetry tasks are never paused.

Three-tier decision loop (reflex / navigation / mission):

  Tier 1 — REFLEX      deterministic table, microseconds, no model in the loop.
                       Resolves every nominal outcome and every hard safety
                       gate.  This is what answers ~all in-flight tool calls.
  Tier 2 — DELIBERATE  ThinkingOracle (qwen3:0.6b via Ollama), consulted only
                       when the reflex tier returns UNKNOWN, under a hard
                       ORACLE_DEADLINE_SEC budget.
  Tier 3 — FALLBACK    _rule_fallback(), mirroring safety_policy.py thresholds,
                       used whenever the oracle is disabled, slow, or unparseable.

Why the tiering matters for latency: planner.decide() runs between the
dispatcher and the tool result the Live model is waiting on, so every
millisecond here lands in the voice round trip.  The oracle used to be invoked
on *every* call while airborne (`_should_invoke_oracle` returned True for
`airborne`), adding a full local LLM generation to each step of a mission.  It
is now reserved for genuinely ambiguous outcomes — repeated failures of
critical tools — where deliberation actually changes the answer.

Zero regression risk on safety: the reflex tier evaluates the same hard gates,
in the same order, that Phase 1/Phase 3 evaluated before; only the decision to
*consult the model* changed.  Build the oracle model with:
    ollama create droneoracle -f thinking_oracle.Modelfile
"""

import asyncio
import json
import logging
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from config import (
    AVOIDANCE_COLLISION_THR, AVOIDANCE_STALE_SEC,
    ORACLE_ENABLED, ORACLE_DEADLINE_SEC, ORACLE_THINK,
    ORACLE_NUM_PREDICT, ORACLE_KEEP_ALIVE, ORACLE_PREWARM,
    BATTERY_CRITICAL_PCT, BATTERY_LOW_PCT, EMERGENCY_STALE_SEC, MAX_RETRY_COUNT,
)
from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy

logger = logging.getLogger(__name__)


# ── Oracle constants ───────────────────────────────────────────────────────────

ORACLE_MODEL   = "droneoracle"
# Advisory only — the planner enforces the real budget with ORACLE_DEADLINE_SEC.
ORACLE_TIMEOUT = ORACLE_DEADLINE_SEC

VALID_DECISIONS = {"CONTINUE", "WAIT", "RETRY", "REPLAN", "ABORT", "FAILSAFE"}

# Tools that warrant oracle deliberation — skip trivial read-only calls
HIGH_VALUE_TOOLS = {
    "goto_position", "takeoff", "return_to_launch",
    "arm_drone", "wait_arrival", "wait_altitude", "land",
}

UNRECOVERABLE_ERRORS = {"ALTITUDE_CEILING", "SPEED_EXCEEDED", "ILLEGAL_COMMAND", "UNKNOWN_TOOL"}


# ── ThinkingDecision ───────────────────────────────────────────────────────────

@dataclass
class ThinkingDecision:
    decision:   str
    reason:     str
    thinking:   str
    next_tool:  Optional[str]   = None
    wait_sec:   Optional[float] = None
    confidence: float           = 1.0
    latency_ms: float           = 0.0
    source:     str             = "oracle"   # "oracle" | "reflex" | "fallback"

    @staticmethod
    def _from_dict(d: dict) -> Optional["ThinkingDecision"]:
        """
        Build a decision from a parsed JSON object, or None if the payload
        does not name a valid decision.

        This lives here because both ThinkingOracle._parse_json and
        ._extract_from_thinking call ``ThinkingDecision._from_dict`` — it was
        only ever defined on ThinkingOracle, so every successful parse raised
        AttributeError.  AttributeError is not in either call site's except
        clause, so it escaped to deliberate()'s catch-all: the oracle paid a
        full generation on every call and then *always* used the rule fallback.
        """
        decision = str(d.get("decision", "")).upper().strip()
        if decision not in VALID_DECISIONS:
            return None
        wait_raw = d.get("wait_sec")
        return ThinkingDecision(
            decision   = decision,
            reason     = str(d.get("reason", ""))[:120],
            thinking   = "",
            next_tool  = d.get("next_tool") or None,
            wait_sec   = float(wait_raw) if wait_raw is not None else None,
            confidence = float(d.get("confidence", 1.0)),
        )


# ── ThinkingOracle ─────────────────────────────────────────────────────────────

class ThinkingOracle:
    """
    Deliberation engine using qwen3:0.6b via Ollama.

    Output grammar is a single compact line — ``DECISION | reason`` — or the
    legacy JSON object; both are accepted.  Chain-of-thought is OFF by default
    (ORACLE_THINK): for a six-way classification the thinking block was ~90% of
    the generated tokens and therefore ~90% of the latency.

    Falls back to deterministic rules (mirroring safety_policy.py) on any failure.
    """

    def __init__(self, model: str = ORACLE_MODEL, timeout: float = ORACLE_TIMEOUT):
        self._model    = model
        self._timeout  = timeout
        self._calls    = 0
        self._failures = 0
        self._prewarmed = False

    def prewarm(self) -> None:
        """
        Load the model into Ollama's memory ahead of the first decision.

        A cold qwen3:0.6b load costs seconds on a Pi-class board, and without
        this the first in-flight decision of every session pays it.
        """
        if self._prewarmed or not ORACLE_PREWARM:
            return
        self._prewarmed = True
        try:
            import ollama
            t0 = time.monotonic()
            ollama.chat(
                model=self._model,
                messages=[{"role": "user", "content": "ping"}],
                think=False,
                stream=False,
                keep_alive=ORACLE_KEEP_ALIVE,
                options={"num_predict": 1, "num_ctx": 256},
            )
            logger.info(
                f"[ORACLE] Prewarmed '{self._model}' in "
                f"{(time.monotonic() - t0) * 1000:.0f}ms "
                f"(keep_alive={ORACLE_KEEP_ALIVE})"
            )
        except Exception as exc:
            logger.warning(f"[ORACLE] Prewarm failed ({exc}) — first call will be cold")

    def deliberate(self, context: dict) -> ThinkingDecision:
        """
        Synchronous deliberation — wrap with asyncio.to_thread() from async callers.

        context keys: tool, ok, error, state, battery_pct, altitude_m,
                      telemetry_age_sec, retry_count, airborne
        """
        import ollama

        self._calls += 1
        t0 = time.monotonic()
        prompt = self._build_prompt(context)

        try:
            thinking_buf = ""
            content_buf  = ""

            options = {
                "temperature": 0.05,
                "num_predict": ORACLE_NUM_PREDICT,
                "num_ctx":     768,
                "top_k":       10,
                "top_p":       0.7,
                # Stop as soon as the single-line verdict ends — without this
                # the model keeps generating up to num_predict every call.
                "stop":        ["\n", "```"],
            }

            if ORACLE_THINK:
                stream = ollama.chat(
                    model=self._model,
                    messages=[{"role": "user", "content": prompt}],
                    think=True,
                    stream=True,
                    keep_alive=ORACLE_KEEP_ALIVE,
                    options=options,
                )
                for chunk in stream:
                    msg = chunk.message
                    if msg.thinking:
                        thinking_buf += msg.thinking
                    if msg.content:
                        content_buf += msg.content
            else:
                resp = ollama.chat(
                    model=self._model,
                    messages=[{"role": "user", "content": prompt}],
                    think=False,
                    stream=False,
                    keep_alive=ORACLE_KEEP_ALIVE,
                    options=options,
                )
                content_buf = getattr(resp.message, "content", "") or ""

            latency_ms = (time.monotonic() - t0) * 1000
            logger.debug(
                f"[ORACLE] Thinking ({latency_ms:.0f}ms):\n"
                f"{thinking_buf[:400]}{'...' if len(thinking_buf) > 400 else ''}"
            )

            decision = (
                self._parse_json(content_buf)
                or self._parse_compact(content_buf)
                or self._extract_from_thinking(thinking_buf)
                or self._parse_compact(thinking_buf)
            )

            if decision:
                decision.thinking   = thinking_buf
                decision.latency_ms = latency_ms
                decision.source     = "oracle"
                logger.info(
                    f"[ORACLE] {context.get('tool')} → {decision.decision} "
                    f"| conf={decision.confidence:.2f} | {decision.reason} "
                    f"| {latency_ms:.0f}ms"
                )
                return decision

            logger.warning(
                f"[ORACLE] Could not parse decision — "
                f"content='{content_buf[:100]}' — using rule fallback"
            )

        except Exception as exc:
            self._failures += 1
            logger.warning(f"[ORACLE] Error: {exc} — rule fallback")

        return self._rule_fallback(context)

    def should_invoke(self, tool_name: str, ok: bool, airborne: bool) -> bool:
        """
        Deprecated — kept for callers outside the planner.

        Being airborne is not by itself ambiguous; the reflex tier
        (``Planner.reflex``) now decides what is worth deliberating on.
        """
        return tool_name in HIGH_VALUE_TOOLS and not ok

    def stats(self) -> dict:
        return {
            "calls":         self._calls,
            "failures":      self._failures,
            "fallback_rate": round(self._failures / max(1, self._calls), 3),
        }

    # ── Prompt ────────────────────────────────────────────────────────────────

    @staticmethod
    def _build_prompt(ctx: dict) -> str:
        return (
            f"tool={ctx.get('tool', 'unknown')} "
            f"ok={ctx.get('ok', True)} "
            f"state={ctx.get('state', 'unknown')} "
            f"error={ctx.get('error') or 'none'} "
            f"battery={ctx.get('battery_pct', 100.0):.1f}% "
            f"altitude={ctx.get('altitude_m', 0.0):.1f}m "
            f"tel_age={ctx.get('telemetry_age_sec', 0.0):.1f}s "
            f"retries={ctx.get('retry_count', 0)} "
            f"airborne={ctx.get('airborne', False)}"
        )

    # ── JSON extraction ───────────────────────────────────────────────────────

    @staticmethod
    def _parse_json(text: str) -> Optional[ThinkingDecision]:
        text = text.strip()
        text = re.sub(r"^```(?:json)?", "", text).rstrip("```").strip()
        if not text:
            return None
        try:
            d = json.loads(text)
            return ThinkingDecision._from_dict(d)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError, AttributeError):
            return None

    @staticmethod
    def _parse_compact(text: str) -> Optional[ThinkingDecision]:
        """
        Parse the compact output grammar: ``DECISION | reason`` (reason optional).

        This is the article's "tiny sentence" form — one verdict token plus an
        optional short justification, instead of a JSON object the model has to
        spell out character by character.
        """
        if not text:
            return None
        for line in text.strip().splitlines():
            token = re.split(r"[\s|:,]+", line.strip(), maxsplit=1)
            if not token:
                continue
            word = token[0].strip().upper().strip("*`\"'")
            if word in VALID_DECISIONS:
                reason = token[1].strip(" |:*`\"'")[:120] if len(token) > 1 else ""
                return ThinkingDecision(
                    decision=word, reason=reason, thinking="", confidence=1.0,
                )
        return None

    @staticmethod
    def _extract_from_thinking(thinking: str) -> Optional[ThinkingDecision]:
        matches = re.findall(r'\{[^{}]*"decision"[^{}]*\}', thinking, re.DOTALL)
        if not matches:
            return None
        for raw in reversed(matches):
            try:
                d = json.loads(raw)
                result = ThinkingDecision._from_dict(d)
                if result:
                    return result
            except (json.JSONDecodeError, KeyError, TypeError, ValueError, AttributeError):
                continue
        return None

    @staticmethod
    def _from_dict(d: dict) -> Optional["ThinkingDecision"]:
        """Alias — the implementation lives on ThinkingDecision."""
        return ThinkingDecision._from_dict(d)

    # ── Deterministic rule fallback ───────────────────────────────────────────

    @staticmethod
    def _rule_fallback(ctx: dict) -> ThinkingDecision:
        """Mirrors safety_policy.py thresholds — zero regression from existing behavior."""
        battery  = ctx.get("battery_pct", 100.0)
        tel_age  = ctx.get("telemetry_age_sec", 0.0)
        retries  = ctx.get("retry_count", 0)
        ok       = ctx.get("ok", True)
        error    = ctx.get("error") or ""
        airborne = ctx.get("airborne", False)

        if tel_age > 10.0 or "TELEMETRY_EMERGENCY" in error:
            decision, reason = "FAILSAFE", f"telemetry age {tel_age:.1f}s exceeds emergency threshold"
        elif battery <= 15.0 or "BATTERY_CRITICAL" in error:
            decision, reason = "FAILSAFE", f"battery critical at {battery:.1f}%"
        elif retries >= 3 or "MAX_RETRIES" in error:
            decision, reason = "ABORT", f"retry limit reached ({retries})"
        elif battery <= 25.0 and airborne:
            decision, reason = "REPLAN", f"battery low at {battery:.1f}% — replan toward RTH"
        elif not ok and retries < 3:
            decision, reason = "RETRY", f"transient failure (retry {retries}/3)"
        else:
            decision, reason = "CONTINUE", "nominal"

        return ThinkingDecision(
            decision   = decision,
            reason     = reason,
            thinking   = "[rule-fallback — oracle unavailable]",
            confidence = 1.0,
            source     = "fallback",
        )


# ── Oracle → PlanDecision mapper ──────────────────────────────────────────────

def _oracle_to_plan(td: ThinkingDecision) -> Optional["PlanDecision"]:
    return {
        "CONTINUE": PlanDecision.CONTINUE,
        "WAIT":     PlanDecision.WAIT,
        "RETRY":    PlanDecision.RETRY,
        "REPLAN":   PlanDecision.REPLAN,
        "ABORT":    PlanDecision.ABORT,
        "FAILSAFE": PlanDecision.FAILSAFE,
    }.get(td.decision)


def build_oracle_context(tool_name: str, resp, sm, safety) -> dict:
    """Shared oracle context builder used by planner and workflows."""
    return {
        "tool":    tool_name,
        "ok":      resp.ok,
        "error":   resp.error,
        "state":   resp.state,
        "airborne": sm.is_airborne(),
        **safety.oracle_context_data(tool_name),
    }


# ── PlanDecision ───────────────────────────────────────────────────────────────

class PlanDecision(str, Enum):
    CONTINUE = "continue"
    WAIT     = "wait"
    RETRY    = "retry"
    REPLAN   = "replan"
    ABORT    = "abort"
    FAILSAFE = "failsafe"


# ── Reflex tier ────────────────────────────────────────────────────────────────

class ReflexVerdict(str, Enum):
    """CHECK grammar — the outcome of the deterministic reflex pass."""
    CLEAR   = "clear"      # nominal; decision is definite
    BLOCKED = "blocked"    # a hard gate fired; decision is definite
    UNKNOWN = "unknown"    # ambiguous; escalate to the oracle


@dataclass
class Reflex:
    verdict:  ReflexVerdict
    decision: Optional[PlanDecision]
    reason:   str

    def is_definite(self) -> bool:
        return self.verdict is not ReflexVerdict.UNKNOWN and self.decision is not None


# ── Planner ────────────────────────────────────────────────────────────────────

class Planner:
    def __init__(self, state_machine: StateMachine, safety_policy: SafetyPolicy, dispatcher):
        self._sm          = state_machine
        self._safety      = safety_policy
        self._dispatcher  = dispatcher
        self._oracle      = ThinkingOracle()
        self._wait:       Optional[WaitInstruction] = None
        self._wait_start: Optional[float] = None
        self._aborted     = False
        self._avoidance_active_since: Optional[float] = None
        # Decision-tier instrumentation (see decision_stats()).
        self._reflex_hits     = 0
        self._escalations     = 0
        self._oracle_timeouts = 0
        self._oracle_busy     = False

    # ── Core decision engine ──────────────────────────────────────────────────

    async def decide(self, response: ToolResponse) -> PlanDecision:
        """
        Three-tier decision pipeline (see module docstring):
          Tier 1 — reflex(): deterministic, microseconds, answers the common case
          Tier 2 — oracle deliberation, only on ReflexVerdict.UNKNOWN, deadlined
          Tier 3 — rule fallback, if the oracle is off / slow / unparseable

        This coroutine sits inside the voice round trip, so the fast path
        deliberately does no I/O and no model call.
        """
        reflex = self.reflex(response)

        if reflex.is_definite():
            self._reflex_hits += 1
            logger.debug(
                f"[PLANNER:REFLEX] {response.tool} → {reflex.decision.value} "
                f"| {reflex.verdict.value} | {reflex.reason}"
            )
            return reflex.decision

        # ── Tier 2: deliberation on genuinely ambiguous outcomes ──────────────
        self._escalations += 1
        td = await self._deliberate(response)
        if td is not None:
            plan_decision = _oracle_to_plan(td)
            if plan_decision:
                if td.wait_sec and plan_decision == PlanDecision.WAIT:
                    response.wait = WaitInstruction(
                        seconds=td.wait_sec,
                        reason=f"oracle: {td.reason}",
                    )
                return plan_decision

        # ── Tier 3: deterministic fallback ────────────────────────────────────
        return self._rule_decision(response)

    # ── Tier 1: reflex ────────────────────────────────────────────────────────

    def reflex(self, response: ToolResponse) -> Reflex:
        """
        Deterministic pass over the same hard gates the old Phase 1/Phase 3
        evaluated.  Pure and synchronous — no I/O, no model, no awaits — so it
        is safe to call from anywhere and costs microseconds.
        """
        # Hard safety gates — always BLOCKED, never deliberated
        if self._sm.state == MissionState.FAILSAFE:
            return Reflex(ReflexVerdict.BLOCKED, PlanDecision.FAILSAFE, "state is failsafe")

        if not response.ok and response.error:
            if any(k in response.error for k in ("BATTERY_CRITICAL", "TELEMETRY_EMERGENCY")):
                return Reflex(ReflexVerdict.BLOCKED, PlanDecision.FAILSAFE, response.error[:80])

        if response.next_action == "emergency":
            return Reflex(ReflexVerdict.BLOCKED, PlanDecision.FAILSAFE, "emergency next_action")

        if not response.ok and self._is_unrecoverable(response):
            return Reflex(ReflexVerdict.BLOCKED, PlanDecision.ABORT, "unrecoverable error")

        # Avoidance gate (DroNet 20 Hz loop)
        avoidance_reflex = self._avoidance_reflex()
        if avoidance_reflex is not None:
            return avoidance_reflex

        # From here the order mirrors the previous Phase 3 exactly, so no
        # decision changes — only *when* the model is consulted changes.

        # Failures: a first transient failure is a plain retry.  Only a
        # *repeated* failure of a flight-critical tool is ambiguous enough that
        # deliberation can change the answer.
        if not response.ok and response.next_action == "retry":
            retries = self._safety.oracle_context_data(response.tool).get("retry_count", 0)
            if response.tool in HIGH_VALUE_TOOLS and retries > 0:
                return Reflex(ReflexVerdict.UNKNOWN, None,
                              f"{response.tool} failed {retries}× — deliberate")
            return Reflex(ReflexVerdict.CLEAR, PlanDecision.RETRY,
                          f"transient failure (retry {retries}/{MAX_RETRY_COUNT})")

        if response.wait:
            return Reflex(ReflexVerdict.CLEAR, PlanDecision.WAIT, response.wait.reason)

        # Live safety monitors — same thresholds as safety_policy.py
        stale = self._safety.check_telemetry_freshness()
        if stale:
            if not stale.retryable:
                return Reflex(ReflexVerdict.BLOCKED, PlanDecision.FAILSAFE, stale.code)
            return Reflex(ReflexVerdict.BLOCKED, PlanDecision.WAIT, stale.code)

        bat = self._safety.check_battery()
        if bat:
            if not bat.retryable:
                return Reflex(ReflexVerdict.BLOCKED, PlanDecision.FAILSAFE, bat.code)
            return Reflex(ReflexVerdict.BLOCKED, PlanDecision.REPLAN, bat.code)

        # Nominal success — definite, and by far the most common path.  This
        # used to cost a full local LLM generation on every airborne call.
        if response.ok:
            return Reflex(ReflexVerdict.CLEAR, PlanDecision.CONTINUE, "nominal")

        return Reflex(ReflexVerdict.UNKNOWN, None, "unclassified failure")

    def _avoidance_reflex(self) -> Optional[Reflex]:
        """WAIT while DroNet is steering; REPLAN if it has been stuck > 10 s."""
        avoidance = self._safety.get_avoidance_state()
        if not self._sm.is_airborne() or avoidance is None:
            return None

        now  = time.monotonic()
        prob = avoidance.collision_prob
        age  = now - avoidance.timestamp

        if prob >= AVOIDANCE_COLLISION_THR and age < AVOIDANCE_STALE_SEC:
            if self._avoidance_active_since is None:
                self._avoidance_active_since = now
            if now - self._avoidance_active_since > 10.0:
                self._avoidance_active_since = None
                logger.warning("[PLANNER] Avoidance stuck >10s — replanning")
                return Reflex(ReflexVerdict.BLOCKED, PlanDecision.REPLAN, "avoidance stuck")
            return Reflex(ReflexVerdict.BLOCKED, PlanDecision.WAIT,
                          f"avoidance active (p={prob:.2f})")

        self._avoidance_active_since = None
        return None

    # ── Tier 2: deliberation, under a hard deadline ───────────────────────────

    async def _deliberate(self, response: ToolResponse) -> Optional[ThinkingDecision]:
        """
        Consult the oracle, but never let it hold up the tool result.

        Two guards the previous version lacked:
          * a real deadline — ORACLE_TIMEOUT was stored and never enforced, so a
            stalled Ollama blocked the voice round trip indefinitely;
          * a single-flight lock — overlapping calls queue behind one another on
            a one-core-per-model backend, so a second caller falls straight
            through to the rules instead of waiting twice as long.
        """
        if not ORACLE_ENABLED:
            return None
        if self._oracle_busy:
            logger.info("[PLANNER] Oracle busy — using rule tier")
            return None

        ctx = build_oracle_context(response.tool, response, self._sm, self._safety)
        self._oracle_busy = True
        t0 = time.monotonic()
        try:
            td: ThinkingDecision = await asyncio.wait_for(
                asyncio.to_thread(self._oracle.deliberate, ctx),
                timeout=ORACLE_DEADLINE_SEC,
            )
        except asyncio.TimeoutError:
            self._oracle_timeouts += 1
            logger.warning(
                f"[PLANNER] Oracle exceeded {ORACLE_DEADLINE_SEC}s deadline "
                f"on '{response.tool}' — using rule tier"
            )
            return None
        except Exception as exc:
            logger.warning(f"[PLANNER] Oracle error: {exc} — using rule tier")
            return None
        finally:
            self._oracle_busy = False

        logger.info(
            f"[PLANNER:ORACLE] {response.tool} → {td.decision} "
            f"| conf={td.confidence:.2f} | src={td.source} | {td.reason} "
            f"| {(time.monotonic() - t0) * 1000:.0f}ms"
        )
        logger.debug(f"[PLANNER:ORACLE:THINKING] {td.thinking[:300]}")
        return td

    async def deliberate_step(self, response: ToolResponse) -> ThinkingDecision:
        """
        Reflex-first step decision for workflows.

        Returns a ThinkingDecision so workflow code that switches on the
        decision strings needs no change.  Workflows used to call the oracle
        unconditionally once per step — a four-step takeoff meant four serial
        local LLM generations.  Now the reflex tier answers nominal steps and
        the oracle is reserved for ambiguous ones, exactly as in decide().
        """
        reflex = self.reflex(response)
        if reflex.is_definite():
            self._reflex_hits += 1
            return ThinkingDecision(
                decision   = reflex.decision.value.upper(),
                reason     = reflex.reason,
                thinking   = "[reflex — no model in the loop]",
                confidence = 1.0,
                source     = "reflex",
            )

        self._escalations += 1
        td = await self._deliberate(response)
        if td is not None:
            return td

        decision = self._rule_decision(response)
        return ThinkingDecision(
            decision   = decision.value.upper(),
            reason     = "rule tier (oracle unavailable)",
            thinking   = "[rule-fallback]",
            confidence = 1.0,
            source     = "fallback",
        )

    # ── Tier 3: rule fallback ─────────────────────────────────────────────────

    @staticmethod
    def _rule_decision(response: ToolResponse) -> PlanDecision:
        """Last resort once reflex was UNKNOWN and the oracle did not answer."""
        if not response.ok and response.next_action == "retry":
            return PlanDecision.RETRY
        if response.wait:
            return PlanDecision.WAIT
        if response.ok:
            return PlanDecision.CONTINUE
        return PlanDecision.ABORT

    # ── Oracle helpers ────────────────────────────────────────────────────────

    def prewarm(self) -> None:
        """Load the oracle model so the first in-flight decision is not cold."""
        self._oracle.prewarm()

    def decision_stats(self) -> dict:
        """How often the reflex tier answered without any model in the loop."""
        total = self._reflex_hits + self._escalations
        return {
            "reflex_hits":     self._reflex_hits,
            "escalations":     self._escalations,
            "oracle_timeouts": self._oracle_timeouts,
            "reflex_rate":     round(self._reflex_hits / max(1, total), 3),
            "oracle":          self._oracle.stats(),
        }

    def _should_invoke_oracle(self, response: ToolResponse) -> bool:
        """Deprecated — superseded by reflex().  Kept for external callers."""
        return not self.reflex(response).is_definite()

    @staticmethod
    def _is_unrecoverable(response: ToolResponse) -> bool:
        return bool(response.error and any(code in response.error for code in UNRECOVERABLE_ERRORS))

    # ── Non-blocking wait ─────────────────────────────────────────────────────

    def schedule_wait(self, wait: WaitInstruction):
        self._wait       = wait
        self._wait_start = time.time()
        logger.info(f"[PLANNER] Wait scheduled: {wait.seconds}s — {wait.reason}")

    def is_waiting(self) -> bool:
        if self._wait is None:
            return False
        elapsed = time.time() - self._wait_start
        if elapsed >= self._wait.seconds:
            logger.info(f"[PLANNER] Wait complete: {self._wait.reason}")
            self._wait       = None
            self._wait_start = None
            return False
        return True

    def wait_remaining(self) -> float:
        if not self._wait:
            return 0.0
        return max(0.0, self._wait.seconds - (time.time() - self._wait_start))

    # ── Workflow runner ───────────────────────────────────────────────────────

    async def run_workflow(self, workflow_fn, *args, **kwargs) -> bool:
        if self._aborted:
            logger.warning("[PLANNER] Workflow blocked — mission aborted.")
            return False
        try:
            return await workflow_fn(
                self._dispatcher, self._sm, self._safety, self, *args, **kwargs
            )
        except Exception as exc:
            logger.exception(f"[PLANNER] Workflow exception: {exc}")
            await self.trigger_failsafe(reason=str(exc))
            return False

    # ── Failsafe ──────────────────────────────────────────────────────────────

    async def trigger_failsafe(self, reason: str = "unknown"):
        logger.critical(f"[PLANNER] ⚠ FAILSAFE — {reason}")
        self._sm.force_failsafe()
        from workflows.emergency import run_emergency
        try:
            await run_emergency(
                self._dispatcher, self._sm, self._safety, self, reason=reason
            )
        except Exception as exc:
            logger.critical(f"[PLANNER] Emergency workflow failed: {exc}")

    def abort(self):
        self._aborted = True
        logger.warning("[PLANNER] Mission aborted by caller.")
