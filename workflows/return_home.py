"""
Return home workflow — sequence:
  1. get_battery
  2. return_to_launch
  3. wait_arrival
  4. land

If battery critical: skip optional steps, go directly to RTL or land.
"""

import asyncio
import logging
from config import BATTERY_CRITICAL_PCT
from planner import PlanDecision

logger = logging.getLogger(__name__)


async def run_return_home(dispatcher, sm, safety, planner) -> bool:
    logger.info("[RTH] Return home initiated")

    # Step 1: Battery check — critical battery skips to fastest safe exit
    bat_resp = await dispatcher.dispatch("get_battery", {})
    battery_pct = bat_resp.data.get("level_percent", 100)

    if battery_pct <= BATTERY_CRITICAL_PCT:
        logger.critical(f"[RTH] Battery critical at {battery_pct}% — skipping to land directly")
        resp = await dispatcher.dispatch("land", {})
        return resp.ok

    # Step 2: Return to launch
    resp = await dispatcher.dispatch("return_to_launch", {})
    decision = planner.decide(resp)
    if decision in (PlanDecision.FAILSAFE, PlanDecision.ABORT):
        await planner.trigger_failsafe(reason=resp.error or "RTL failed")
        return False
    if resp.wait:
        planner.schedule_wait(resp.wait)
        while planner.is_waiting():
            await asyncio.sleep(0.2)

    # Step 3: Wait arrival at home
    resp = await dispatcher.dispatch("wait_arrival", {})
    if not resp.ok:
        logger.warning(f"[RTH] wait_arrival uncertain: {resp.error}")

    # Step 4: Land
    resp = await dispatcher.dispatch("land", {})
    if not resp.ok:
        logger.error(f"[RTH] land failed: {resp.error}")
        return False

    logger.info("[RTH] ✓ Home — landed")
    return True
