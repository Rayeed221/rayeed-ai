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
"""

import asyncio
import logging
import time
from enum import Enum
from typing import Optional

from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy

logger = logging.getLogger(__name__)


class PlanDecision(str, Enum):
    CONTINUE = "continue"
    WAIT     = "wait"
    RETRY    = "retry"
    REPLAN   = "replan"
    ABORT    = "abort"
    FAILSAFE = "failsafe"


class Planner:
    def __init__(self, state_machine: StateMachine, safety_policy: SafetyPolicy, dispatcher):
        self._sm         = state_machine
        self._safety     = safety_policy
        self._dispatcher = dispatcher
        self._wait:      Optional[WaitInstruction] = None
        self._wait_start: Optional[float] = None
        self._aborted    = False

    # ── Core decision engine (planner overrides LLM) ──────────────────────────

    def decide(self, response: ToolResponse) -> PlanDecision:
        """
        Evaluate a ToolResponse and return one of the six plan outcomes.
        Planner authority: safety-critical cases override LLM next_action.
        """
        state = self._sm.state

        # 1. Already in failsafe — don't advance anything
        if state == MissionState.FAILSAFE:
            return PlanDecision.FAILSAFE

        # 2. Emergency triggers (planner overrides LLM)
        if not response.ok and response.error:
            if any(k in response.error for k in ("BATTERY_CRITICAL", "TELEMETRY_EMERGENCY")):
                return PlanDecision.FAILSAFE

        # 3. Non-retryable failure → abort
        if not response.ok and response.next_action not in ("retry", "emergency"):
            return PlanDecision.ABORT

        # 4. Emergency next_action → failsafe
        if response.next_action == "emergency":
            return PlanDecision.FAILSAFE

        # 5. Retryable failure
        if not response.ok and response.next_action == "retry":
            return PlanDecision.RETRY

        # 6. Wait instruction present
        if response.wait:
            return PlanDecision.WAIT

        # 7. Telemetry freshness check (planner injects wait)
        stale = self._safety.check_telemetry_freshness()
        if stale:
            return PlanDecision.FAILSAFE if not stale.retryable else PlanDecision.WAIT

        # 8. Battery warning (planner injects replan toward RTH)
        bat = self._safety.check_battery()
        if bat and not bat.retryable:
            return PlanDecision.FAILSAFE

        # 9. Success with next action → continue
        if response.ok:
            return PlanDecision.CONTINUE

        return PlanDecision.ABORT

    # ── Non-blocking wait ──────────────────────────────────────────────────────

    def schedule_wait(self, wait: WaitInstruction):
        """Schedule a non-blocking wait. Audio + telemetry continue normally."""
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

    # ── Workflow runner ────────────────────────────────────────────────────────

    async def run_workflow(self, workflow_fn, *args, **kwargs) -> bool:
        """Run a code-driven workflow coroutine. Returns True on success."""
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

    # ── Failsafe (planner authority — overrides everything) ───────────────────

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
