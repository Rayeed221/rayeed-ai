"""
Takeoff workflow — sequence:
  1. set_mode(GUIDED)
  2. arm_drone
  3. takeoff(altitude)
  4. wait_altitude(altitude)

If altitude not stable: wait → recheck → retry or failsafe.
"""

import asyncio
import logging
from planner import PlanDecision

logger = logging.getLogger(__name__)


async def _step(dispatcher, planner, tool_name: str, args: dict) -> bool:
    """Dispatch a tool, handle wait and planner decision. Returns False on abort."""
    resp = await dispatcher.dispatch(tool_name, args)
    decision = planner.decide(resp)
    logger.info(f"[TAKEOFF] {tool_name} → ok={resp.ok} decision={decision.value}")

    if decision == PlanDecision.WAIT and resp.wait:
        planner.schedule_wait(resp.wait)
        while planner.is_waiting():
            await asyncio.sleep(0.2)

    elif decision in (PlanDecision.FAILSAFE, PlanDecision.ABORT):
        await planner.trigger_failsafe(reason=resp.error or f"{tool_name} failed")
        return False

    elif decision == PlanDecision.RETRY:
        logger.warning(f"[TAKEOFF] Retrying {tool_name}")
        return await _step(dispatcher, planner, tool_name, args)

    return resp.ok


async def run_takeoff(dispatcher, sm, safety, planner, altitude: float = 10.0) -> bool:
    logger.info(f"[TAKEOFF] Initiating takeoff to {altitude}m")

    if not await _step(dispatcher, planner, "set_mode", {"mode": "GUIDED"}):
        return False

    if not await _step(dispatcher, planner, "arm_drone", {}):
        return False

    if not await _step(dispatcher, planner, "takeoff", {"altitude": altitude}):
        return False

    # Wait for altitude — retry up to MAX_RETRY_COUNT if not stable
    if not await _step(dispatcher, planner, "wait_altitude", {"target_alt": altitude}):
        return False

    logger.info(f"[TAKEOFF] ✓ Complete — hovering at {altitude}m")
    return True
