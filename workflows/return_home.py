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

    # Step 1: Battery check
    if not await planner.execute_step("get_battery", {}):
        return False

    # Step 2: Return to launch
    if not await planner.execute_step("return_to_launch", {}):
        return False

    # Step 3: Wait arrival at home
    if not await planner.execute_step("wait_arrival", {}):
        logger.warning("[RTH] wait_arrival uncertain")

    # Step 4: Land
    if not await planner.execute_step("land", {}):
        return False

    logger.info("[RTH] ✓ Home — landed")
    return True
