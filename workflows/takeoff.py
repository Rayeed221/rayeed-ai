"""
Takeoff workflow — sequence:
  1. set_mode(GUIDED)
  2. arm_drone
  3. takeoff(altitude)
  4. wait_altitude(altitude)

Each step is dispatched in order; a failed step aborts the workflow. The
planner's decision engine (safety gates + avoidance) governs in-flight
decisions separately.
"""

import logging

logger = logging.getLogger(__name__)


async def run_takeoff(dispatcher, sm, safety, planner, altitude: float = 10.0) -> bool:
    logger.info(f"[TAKEOFF] Initiating takeoff to {altitude}m")

    steps = [
        ("set_mode",      {"mode": "GUIDED"}),
        ("arm_drone",     {}),
        ("takeoff",       {"altitude": altitude}),
        ("wait_altitude", {"target_alt": altitude}),
    ]

    for tool_name, args in steps:
        resp = await dispatcher.dispatch(tool_name, args)
        if not resp.ok:
            logger.error(f"[TAKEOFF] Failed at step {tool_name}: {resp.error}")
            return False
        logger.info(f"[TAKEOFF] ✓ {tool_name} — data={resp.data}")

    logger.info(f"[TAKEOFF] ✓ Complete — hovering at {altitude}m")
    return True
