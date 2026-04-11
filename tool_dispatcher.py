"""
Dispatcher flow (Decision 4 — Planner has override authority):

  incoming tool call
  → validate against registry
  → safety pre-check (battery / telemetry / altitude / speed / legality / retries)
  → execute via backend adapter (with timeout)
  → normalize to ToolResponse schema
  → update mission state machine
  → update safety monitors
  → return ToolResponse to caller
"""

import asyncio
import logging

from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState, IllegalTransitionError
from safety_policy import SafetyPolicy
from tool_registry import TOOL_REGISTRY

logger = logging.getLogger(__name__)

# ── State transitions triggered by specific tools ─────────────────────────────
TOOL_STATE_TRANSITIONS = {
    "connect_drone":    MissionState.CONNECTED,
    "arm_drone":        MissionState.ARMED,
    "takeoff":          MissionState.TAKEOFF,
    "wait_altitude":    MissionState.HOVER,
    "goto_position":    MissionState.ENROUTE,
    "return_to_launch": MissionState.RTL,
    "land":             MissionState.LANDING,
    "disarm_drone":     MissionState.IDLE,
}

# ── Next action hints returned to planner / LLM ──────────────────────────────
TOOL_NEXT_ACTION = {
    "connect_drone":    "get_current_state",
    "arm_drone":        "takeoff",
    "takeoff":          "wait_altitude",
    "wait_altitude":    "get_telemetry",
    "goto_position":    "wait_arrival",
    "return_to_launch": "wait_arrival",
    "land":             "disarm_drone",
    "wait_arrival":     "get_telemetry",
}

# ── Wait hints appended to response (non-blocking — planner schedules these) ──
TOOL_WAIT_HINTS = {
    "arm_drone":        WaitInstruction(seconds=1.0,  reason="motor spin-up"),
    "takeoff":          WaitInstruction(seconds=2.0,  reason="allow altitude to stabilize"),
    "set_mode":         WaitInstruction(seconds=0.5,  reason="mode change propagation"),
    "goto_position":    WaitInstruction(seconds=1.0,  reason="navigation initialization"),
    "return_to_launch": WaitInstruction(seconds=2.0,  reason="RTL initialization"),
}

TOOL_TIMEOUT_SEC = 10.0


class ToolDispatcher:
    def __init__(self, state_machine: StateMachine, safety_policy: SafetyPolicy, adapter):
        self._sm                   = state_machine
        self._safety               = safety_policy
        self._adapter              = adapter
        self._avoidance_controller = None  # set via set_avoidance_controller()

    def set_avoidance_controller(self, controller) -> None:
        """Register an AvoidanceController to intercept goto_position calls."""
        self._avoidance_controller = controller
        logger.info("[DISPATCH] AvoidanceController registered")

    async def dispatch(self, tool_name: str, args: dict) -> ToolResponse:
        current_state = self._sm.state

        # ── 1. Registry check ─────────────────────────────────────────────────
        if tool_name not in TOOL_REGISTRY:
            return ToolResponse.failure(
                tool=tool_name, state=current_state.value,
                error=f"Tool '{tool_name}' not in registry",
                next_action="get_current_state",
            )

        # ── 2. Safety pre-check (planner authority: block before execution) ───
        err = self._safety.pre_execute_check(tool_name, args)
        if err:
            logger.error(f"[DISPATCH] Safety block [{err.code}]: {err.message}")
            emergency_triggers = {"BATTERY_CRITICAL", "TELEMETRY_EMERGENCY", "MAX_RETRIES"}
            return ToolResponse.failure(
                tool=tool_name, state=current_state.value,
                error=err.message,
                next_action="emergency" if err.code in emergency_triggers else "retry" if err.retryable else None,
                confidence=0.0,
            )

        # ── 2b. Avoidance intercept for goto_position ─────────────────────────
        if tool_name == "goto_position" and self._avoidance_controller is not None:
            try:
                await self._avoidance_controller.set_goal(
                    args["lat"], args["lon"], args["alt"]
                )
                reached = await self._avoidance_controller.wait_for_arrival(timeout=120.0)
            except Exception as exc:
                logger.exception(f"[DISPATCH] AvoidanceController error: {exc}")
                self._safety.increment_retry(tool_name)
                return ToolResponse.failure(
                    tool=tool_name, state=current_state.value,
                    error=f"avoidance error: {exc}",
                    next_action="retry",
                )

            # State transition
            new_state = TOOL_STATE_TRANSITIONS.get(tool_name)
            if new_state:
                try:
                    self._sm.transition(new_state)
                except IllegalTransitionError as exc:
                    logger.warning(f"[DISPATCH] State transition skipped: {exc}")

            self._safety.reset_retry(tool_name)
            logger.info(f"[DISPATCH] ✓ goto_position (avoidance) → state={self._sm.state.value}")

            return ToolResponse.success(
                tool=tool_name,
                state=self._sm.state.value,
                data={
                    "status": "reached" if reached else "timeout",
                    "avoidance": True,
                },
                next_action=TOOL_NEXT_ACTION.get(tool_name),
                wait=TOOL_WAIT_HINTS.get(tool_name),
                confidence=1.0 if reached else 0.5,
            )

        # ── 3. Execute via adapter with timeout ───────────────────────────────
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(self._adapter.execute, tool_name, args),
                timeout=TOOL_TIMEOUT_SEC,
            )
        except asyncio.TimeoutError:
            self._safety.increment_retry(tool_name)
            logger.warning(f"[DISPATCH] Timeout: {tool_name}")
            return ToolResponse.failure(
                tool=tool_name, state=current_state.value,
                error=f"'{tool_name}' timed out after {TOOL_TIMEOUT_SEC}s",
                next_action="retry",
            )
        except Exception as exc:
            self._safety.increment_retry(tool_name)
            logger.exception(f"[DISPATCH] Exception in '{tool_name}': {exc}")
            return ToolResponse.failure(
                tool=tool_name, state=current_state.value,
                error=str(exc), next_action="retry",
            )

        # Check adapter-level error
        if "error" in result:
            self._safety.increment_retry(tool_name)
            return ToolResponse.failure(
                tool=tool_name, state=current_state.value,
                error=result["error"], next_action="retry",
            )

        # ── 4. State transition ────────────────────────────────────────────────
        new_state = TOOL_STATE_TRANSITIONS.get(tool_name)
        if new_state:
            try:
                self._sm.transition(new_state)
            except IllegalTransitionError as exc:
                logger.warning(f"[DISPATCH] State transition skipped: {exc}")

        # ── 5. Update safety monitors ──────────────────────────────────────────
        if tool_name in ("get_telemetry", "get_current_state"):
            self._safety.update_telemetry_timestamp()
        if tool_name == "get_battery" and "level_percent" in result:
            self._safety.update_battery(result["level_percent"])
        if tool_name == "get_telemetry" and "altitude" in result:
            self._safety.update_altitude(result["altitude"])

        # ── 6. Reset retry counter on success ─────────────────────────────────
        self._safety.reset_retry(tool_name)

        logger.info(f"[DISPATCH] ✓ {tool_name} → state={self._sm.state.value}")

        # ── 7. Normalize and return ────────────────────────────────────────────
        return ToolResponse.success(
            tool=tool_name,
            state=self._sm.state.value,
            data=result,
            next_action=TOOL_NEXT_ACTION.get(tool_name),
            wait=TOOL_WAIT_HINTS.get(tool_name),
            confidence=1.0,
        )
