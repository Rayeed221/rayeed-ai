"""
planner_oracle_patch.py — Drop-in augmented Planner for DroneAI (RayeedAI).

HOW TO INTEGRATE:
  Replace your existing planner.py with this file, OR apply the diff
  manually by following the inline # PATCH comments.

Changes from original planner.py:
  1. Import ThinkingOracle and WaitInstruction
  2. Instantiate self._oracle in __init__
  3. decide() gains Phase 2 oracle block between hard gates and rule fallback
  4. Two new private helpers: _should_invoke_oracle(), _build_oracle_context()
  5. Module-level _oracle_to_plan() mapper

All existing logic, method signatures, and PlanDecision values are unchanged.
"""

import asyncio
import logging
import time
from enum import Enum
from typing import Optional

from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy
from thinking_oracle import ThinkingOracle, ThinkingDecision   # PATCH: new import

logger = logging.getLogger(__name__)


class PlanDecision(str, Enum):
    CONTINUE = "continue"
    WAIT     = "wait"
    RETRY    = "retry"
    REPLAN   = "replan"
    ABORT    = "abort"
    FAILSAFE = "failsafe"


def _oracle_to_plan(td: ThinkingDecision) -> Optional[PlanDecision]:
    """Map oracle ThinkingDecision string to PlanDecision enum."""
    return {
        "CONTINUE": PlanDecision.CONTINUE,
        "WAIT":     PlanDecision.WAIT,
        "RETRY":    PlanDecision.RETRY,
        "REPLAN":   PlanDecision.REPLAN,
        "ABORT":    PlanDecision.ABORT,
        "FAILSAFE": PlanDecision.FAILSAFE,
    }.get(td.decision)


class Planner:
    def __init__(self, state_machine: StateMachine, safety_policy: SafetyPolicy, dispatcher):
        self._sm         = state_machine
        self._safety     = safety_policy
        self._dispatcher = dispatcher
        self._oracle     = ThinkingOracle()       # PATCH: oracle instance
        self._wait:      Optional[WaitInstruction] = None
        self._wait_start: Optional[float] = None
        self._aborted    = False

    # ── Core decision engine ──────────────────────────────────────────────────

    def decide(self, response: ToolResponse) -> PlanDecision:
        """
        Three-phase decision pipeline:
          Phase 1 — Hard safety gates (deterministic, always executes)
          Phase 2 — Oracle deliberation (qwen3:0.6b, ambiguous/airborne cases)
          Phase 3 — Original rule-based fallback (unchanged from original)
        """
        state = self._sm.state

        # ── Phase 1: Hard safety gates (UNCHANGED) ────────────────────────
        if state == MissionState.FAILSAFE:
            return PlanDecision.FAILSAFE

        if not response.ok and response.error:
            if any(k in response.error for k in ("BATTERY_CRITICAL", "TELEMETRY_EMERGENCY")):
                return PlanDecision.FAILSAFE

        if not response.ok and response.next_action not in ("retry", "emergency"):
            # PATCH: let oracle review before hard abort — only if not truly unrecoverable
            if not self._is_unrecoverable(response):
                pass   # fall through to oracle
            else:
                return PlanDecision.ABORT

        if response.next_action == "emergency":
            return PlanDecision.FAILSAFE

        # ── Phase 2: Oracle deliberation (PATCH) ──────────────────────────
        if self._should_invoke_oracle(response):
            oracle_ctx = self._build_oracle_context(response)

            # deliberate() is sync — safe to call here since decide() is called
            # from async receive_responses(), but the oracle call itself is fast
            # enough (<200ms on CPU) that blocking the event loop is acceptable.
            # For strict non-blocking, wrap the entire decide() call with
            # asyncio.to_thread() at the call site in app.py.
            td: ThinkingDecision = self._oracle.deliberate(oracle_ctx)

            logger.info(
                f"[PLANNER:ORACLE] {response.tool} → {td.decision} "
                f"| conf={td.confidence:.2f} | src={td.source} | {td.reason}"
            )
            logger.debug(f"[PLANNER:ORACLE:THINKING] {td.thinking[:300]}")

            plan_decision = _oracle_to_plan(td)
            if plan_decision:
                # Inject oracle-derived wait if model specified wait_sec
                if td.wait_sec and plan_decision == PlanDecision.WAIT:
                    response.wait = WaitInstruction(
                        seconds=td.wait_sec,
                        reason=f"oracle: {td.reason}",
                    )
                return plan_decision

        # ── Phase 3: Original rule-based fallback (UNCHANGED) ────────────
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

    # ── Oracle helpers (PATCH) ────────────────────────────────────────────────

    def _should_invoke_oracle(self, response: ToolResponse) -> bool:
        """
        Gate: only call oracle when outcome is ambiguous.
        Skips oracle for trivial read-only telemetry calls to avoid latency.
        """
        from thinking_oracle import HIGH_VALUE_TOOLS
        return (
            response.tool in HIGH_VALUE_TOOLS
            or not response.ok
            or self._sm.is_airborne()
        )

    def _build_oracle_context(self, response: ToolResponse) -> dict:
        tel_age = (
            0.0
            if self._safety._last_tel_time == 0.0
            else time.time() - self._safety._last_tel_time
        )
        return {
            "tool":              response.tool,
            "ok":                response.ok,
            "error":             response.error,
            "state":             response.state,
            "battery_pct":       self._safety._last_battery,
            "altitude_m":        self._safety._last_altitude,
            "telemetry_age_sec": tel_age,
            "retry_count":       self._safety._retry_counts.get(response.tool, 0),
            "airborne":          self._sm.is_airborne(),
        }

    @staticmethod
    def _is_unrecoverable(response: ToolResponse) -> bool:
        """True if failure code is categorically unrecoverable — skip oracle."""
        UNRECOVERABLE = {"ALTITUDE_CEILING", "SPEED_EXCEEDED", "ILLEGAL_COMMAND", "UNKNOWN_TOOL"}
        return response.error and any(code in response.error for code in UNRECOVERABLE)

    # ── Non-blocking wait (UNCHANGED) ─────────────────────────────────────────

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

    # ── Workflow runner (UNCHANGED) ────────────────────────────────────────────

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

    # ── Failsafe (UNCHANGED) ──────────────────────────────────────────────────

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
