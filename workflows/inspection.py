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
    resp = await dispatcher.dispatch("wait_time", {"seconds": hold_seconds})
    if resp.wait:
        planner.schedule_wait(resp.wait)
        while planner.is_waiting():
            await asyncio.sleep(0.2)

    # Step 2: Orient (optional)
    if yaw_deg is not None:
        resp = await dispatcher.dispatch("set_yaw", {"yaw_deg": yaw_deg})
        logger.info(f"[INSPECTION] Yaw set → {resp.data}")

    # Step 3: Read position
    pos_resp = await dispatcher.dispatch("get_position_str", {})
    logger.info(f"[INSPECTION] Position: {pos_resp.data.get('position')}")

    # Step 4: Read telemetry
    tel_resp = await dispatcher.dispatch("get_telemetry", {})
    logger.info(f"[INSPECTION] Telemetry: {tel_resp.data}")

    logger.info("[INSPECTION] ✓ Complete")
    return True
