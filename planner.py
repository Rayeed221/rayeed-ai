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

import logging
import time
from enum import Enum
from typing import Optional

from config import AVOIDANCE_COLLISION_THR, AVOIDANCE_STALE_SEC
from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy

logger = logging.getLogger(__name__)


UNRECOVERABLE_ERRORS = {"ALTITUDE_CEILING", "SPEED_EXCEEDED", "ILLEGAL_COMMAND", "UNKNOWN_TOOL"}


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
        self._wait:       Optional[WaitInstruction] = None
        self._wait_start: Optional[float] = None
        self._aborted     = False
        self._avoidance_active_since: Optional[float] = None

    # ── Core decision engine ──────────────────────────────────────────────────

    def decide(self, response: ToolResponse) -> PlanDecision:
        """
        Two-phase deterministic decision pipeline:
          Phase 1  — Hard safety gates (always executes)
          Phase 1b — Avoidance gate (DroNet 20 Hz loop)
          Phase 2  — Rule-based decision
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
            # fall through to the rule-based decision for ambiguous failures

        # ── Phase 1b: Avoidance gate (DroNet 20 Hz loop) ─────────────────────
        avoidance = self._safety.get_avoidance_state()
        if self._sm.is_airborne() and avoidance is not None:
            now  = time.monotonic()
            prob = avoidance.collision_prob
            age  = now - avoidance.timestamp
            if prob >= AVOIDANCE_COLLISION_THR and age < AVOIDANCE_STALE_SEC:
                if self._avoidance_active_since is None:
                    self._avoidance_active_since = now
                if now - self._avoidance_active_since > 10.0:
                    self._avoidance_active_since = None
                    logger.warning("[PLANNER] Avoidance stuck >10s — replanning")
                    return PlanDecision.REPLAN
                return PlanDecision.WAIT
            else:
                self._avoidance_active_since = None

        # ── Phase 2: Rule-based decision ──────────────────────────────────────
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

    # ── Helpers ───────────────────────────────────────────────────────────────

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
