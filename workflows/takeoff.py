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


async def run_takeoff(dispatcher, sm, safety, planner, altitude: float = 10.0) -> bool:
    logger.info(f"[TAKEOFF] Initiating takeoff to {altitude}m")

    if not await planner.execute_step("set_mode", {"mode": "GUIDED"}):
        return False

    if not await planner.execute_step("arm_drone", {}):
        return False

    if not await planner.execute_step("takeoff", {"altitude": altitude}):
        return False

    # Wait for altitude
    if not await planner.execute_step("wait_altitude", {"target_alt": altitude}):
        return False

    logger.info(f"[TAKEOFF] ✓ Complete — hovering at {altitude}m")
    return True
