"""
Inspection workflow — sequence:
  1. wait_time  (hold position for data capture)
  2. set_yaw    (optional — orient toward target)
  3. get_position_str
  4. get_telemetry
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def run_inspection(
    dispatcher, sm, safety, planner,
    hold_seconds: float = 10.0,
    yaw_deg:      float = None,
) -> bool:
    logger.info(f"[INSPECTION] Holding {hold_seconds}s for data capture")

    # Step 1: Hold position
    await planner.execute_step("wait_time", {"seconds": hold_seconds})

    # Step 2: Orient (optional)
    if yaw_deg is not None:
        await planner.execute_step("set_yaw", {"yaw_deg": yaw_deg})

    # Step 3: Read position
    await planner.execute_step("get_position_str", {})

    # Step 4: Read telemetry
    await planner.execute_step("get_telemetry", {})

    logger.info("[INSPECTION] ✓ Complete")
    return True
