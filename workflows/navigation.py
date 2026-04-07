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

    # Step 1: Set speed
    await planner.execute_step("set_speed", {"speed_ms": speed_ms})

    # Step 2: Set yaw (optional)
    if yaw_deg is not None:
        await planner.execute_step("set_yaw", {"yaw_deg": yaw_deg})

    # Step 3: Goto position
    if not await planner.execute_step("goto_position", {"lat": lat, "lon": lon, "alt": alt}):
        return False

    # Step 4: Wait arrival
    if not await planner.execute_step("wait_arrival", {}):
        return False

    logger.info("[NAV] ✓ Arrived at target")
    return True
