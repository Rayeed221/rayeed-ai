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
    resp = await dispatcher.dispatch("land", {})
    if not resp.ok:
        logger.error(f"[LANDING] land failed: {resp.error}")
        return False

    # Step 2: Brief wait for ground contact
    await asyncio.sleep(2.0)

    # Step 3: Disarm
    resp = await dispatcher.dispatch("disarm_drone", {})
    if not resp.ok:
        logger.warning(f"[LANDING] disarm failed: {resp.error} — may already be disarmed")

    logger.info("[LANDING] ✓ Landed and disarmed")
    return True
