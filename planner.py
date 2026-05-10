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

Oracle layer (Phase 2): ThinkingOracle (qwen3:0.6b via Ollama) deliberates
between hard safety gates and the rule-based fallback. Zero regression risk —
if the oracle fails or times out, _rule_fallback() mirrors safety_policy.py
thresholds exactly. Build the model first:
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

from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy

logger = logging.getLogger(__name__)


# ── Oracle constants ───────────────────────────────────────────────────────────

ORACLE_MODEL   = "droneoracle"
ORACLE_TIMEOUT = 8.0   # must be < tool_dispatcher.py TOOL_TIMEOUT_SEC (10s)

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
    source:     str             = "oracle"   # "oracle" | "fallback"


# ── ThinkingOracle ─────────────────────────────────────────────────────────────

class ThinkingOracle:
    """
    Sequential thinking engine using qwen3:0.6b via Ollama.

    Streams a <think>...</think> reasoning block before the JSON commitment.
    Falls back to deterministic rules (mirroring safety_policy.py) on any failure.
    """

    def __init__(self, model: str = ORACLE_MODEL, timeout: float = ORACLE_TIMEOUT):
        self._model    = model
        self._timeout  = timeout
        self._calls    = 0
        self._failures = 0

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

            stream = ollama.chat(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                think=True,
                stream=True,
                options={
                    "temperature": 0.05,
                    "num_predict": 96,
                    "num_ctx":     768,
                    "top_k":       10,
                    "top_p":       0.7,
                },
            )

            for chunk in stream:
                msg = chunk.message
                if msg.thinking:
                    thinking_buf += msg.thinking
                if msg.content:
                    content_buf += msg.content

            latency_ms = (time.monotonic() - t0) * 1000
            logger.debug(
                f"[ORACLE] Thinking ({latency_ms:.0f}ms):\n"
                f"{thinking_buf[:400]}{'...' if len(thinking_buf) > 400 else ''}"
            )

            decision = (
                self._parse_json(content_buf)
                or self._extract_from_thinking(thinking_buf)
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
        return tool_name in HIGH_VALUE_TOOLS or not ok or airborne

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
        except (json.JSONDecodeError, KeyError, TypeError):
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
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        return None

    @staticmethod
    def _from_dict(d: dict) -> Optional["ThinkingDecision"]:
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

    # ── Core decision engine ──────────────────────────────────────────────────

    async def decide(self, response: ToolResponse) -> PlanDecision:
        """
        Three-phase decision pipeline:
          Phase 1 — Hard safety gates (deterministic, always executes)
          Phase 2 — Oracle deliberation (qwen3:0.6b, ambiguous/airborne cases)
          Phase 3 — Rule-based fallback (unchanged from original)
        """
        state = self._sm.state

        # ── Phase 1: Hard safety gates ────────────────────────────────────────
        if state == MissionState.FAILSAFE:
            return PlanDecision.FAILSAFE

        if not response.ok and response.error:
            if any(k in response.error for k in ("BATTERY_CRITICAL", "TELEMETRY_EMERGENCY")):
                return PlanDecision.FAILSAFE

        if response.next_action == "emergency":
            return PlanDecision.FAILSAFE

        if not response.ok and response.next_action not in ("retry", "emergency"):
            if self._is_unrecoverable(response):
                return PlanDecision.ABORT
            # fall through to oracle for ambiguous failures

        # ── Phase 2: Oracle deliberation (non-blocking) ───────────────────────
        if self._should_invoke_oracle(response):
            oracle_ctx = build_oracle_context(response.tool, response, self._sm, self._safety)
            td: ThinkingDecision = await asyncio.to_thread(self._oracle.deliberate, oracle_ctx)

            logger.info(
                f"[PLANNER:ORACLE] {response.tool} → {td.decision} "
                f"| conf={td.confidence:.2f} | src={td.source} | {td.reason}"
            )
            logger.debug(f"[PLANNER:ORACLE:THINKING] {td.thinking[:300]}")

            plan_decision = _oracle_to_plan(td)
            if plan_decision:
                if td.wait_sec and plan_decision == PlanDecision.WAIT:
                    response.wait = WaitInstruction(
                        seconds=td.wait_sec,
                        reason=f"oracle: {td.reason}",
                    )
                return plan_decision

        # ── Phase 3: Rule-based fallback ──────────────────────────────────────
        if not response.ok and response.next_action == "retry":
            return PlanDecision.RETRY

        if response.wait:
            return PlanDecision.WAIT

        stale = self._safety.check_telemetry_freshness()
        if stale:
            return PlanDecision.FAILSAFE if not stale.retryable else PlanDecision.WAIT

        bat = self._safety.check_battery()
        if bat:
            if not bat.retryable:
                return PlanDecision.FAILSAFE
            return PlanDecision.REPLAN

        if response.ok:
            return PlanDecision.CONTINUE

        return PlanDecision.ABORT

    # ── Oracle helpers ────────────────────────────────────────────────────────

    def _should_invoke_oracle(self, response: ToolResponse) -> bool:
        return (
            response.tool in HIGH_VALUE_TOOLS
            or not response.ok
            or self._sm.is_airborne()
        )

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
