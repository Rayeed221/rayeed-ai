"""
Navigation workflow — sequence:
  1. set_speed
  2. set_yaw  (optional)
  3. goto_position
  4. wait_arrival

If target is far or uncertain: wait → re-read position → continue or replan.
"""

import asyncio
import logging
from planner import PlanDecision

logger = logging.getLogger(__name__)


async def run_navigation(
    dispatcher, sm, safety, planner,
    lat: float, lon: float, alt: float,
    speed_ms: float = 5.0,
    yaw_deg:  float = None,
) -> bool:
    logger.info(f"[NAV] Navigating to ({lat:.6f}, {lon:.6f}, {alt}m) @ {speed_ms} m/s")

    # Step 1: Set speed (non-critical — warn and continue on failure)
    resp = await dispatcher.dispatch("set_speed", {"speed_ms": speed_ms})
    if not resp.ok:
        logger.warning(f"[NAV] set_speed failed: {resp.error} — continuing anyway")

    # Step 2: Set yaw (optional)
    if yaw_deg is not None:
        resp = await dispatcher.dispatch("set_yaw", {"yaw_deg": yaw_deg})
        if resp.wait:
            planner.schedule_wait(resp.wait)
            while planner.is_waiting():
                await asyncio.sleep(0.2)

    # Step 3: Goto position
    resp = await dispatcher.dispatch("goto_position", {"lat": lat, "lon": lon, "alt": alt})
    decision = planner.decide(resp)
    if decision in (PlanDecision.FAILSAFE, PlanDecision.ABORT):
        await planner.trigger_failsafe(reason=resp.error or "goto_position failed")
        return False
    if resp.wait:
        planner.schedule_wait(resp.wait)
        while planner.is_waiting():
            await asyncio.sleep(0.2)

    # Step 4: Wait arrival — re-check position if needed
    resp = await dispatcher.dispatch("wait_arrival", {})
    if not resp.ok:
        logger.warning("[NAV] wait_arrival uncertain — re-reading position")
        pos = await dispatcher.dispatch("get_position_str", {})
        logger.info(f"[NAV] Current position: {pos.data}")
        # Re-attempt arrival check once
        resp = await dispatcher.dispatch("wait_arrival", {})
        if not resp.ok:
            logger.error("[NAV] Arrival confirmation failed")
            return False

    logger.info("[NAV] ✓ Arrived at target")
    return True
