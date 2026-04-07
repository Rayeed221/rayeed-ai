"""
Landing workflow — sequence:
  1. land
  2. wait (ground contact confirmation)
  3. disarm_drone
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def run_landing(dispatcher, sm, safety, planner) -> bool:
    logger.info("[LANDING] Initiating landing")

    # Step 1: Land command
    if not await planner.execute_step("land", {}):
        return False

    # Step 2: Brief wait for ground contact
    await asyncio.sleep(2.0)

    # Step 3: Disarm
    await planner.execute_step("disarm_drone", {})

    logger.info("[LANDING] ✓ Landed and disarmed")
    return True
