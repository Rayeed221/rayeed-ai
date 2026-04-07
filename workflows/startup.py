"""
Startup workflow — sequence:
  1. connect_drone
  2. get_current_state
  3. get_telemetry
  4. get_battery
  5. set_mode(GUIDED)
"""

import asyncio
import logging

logger = logging.getLogger(__name__)

_STEPS = [
    ("connect_drone",    lambda cs: {"connection_string": cs}),
    ("get_current_state", lambda _: {}),
    ("get_telemetry",     lambda _: {}),
    ("get_battery",       lambda _: {}),
    ("set_mode",          lambda _: {"mode": "GUIDED"}),
]


async def run_startup(dispatcher, sm, safety, planner, connection_string="udp:127.0.0.1:14550") -> bool:
    logger.info("[STARTUP] Initiating startup workflow")

    for tool_name, arg_fn in _STEPS:
        if not await planner.execute_step(tool_name, arg_fn(connection_string)):
            logger.error(f"[STARTUP] Aborted at '{tool_name}'")
            return False

    logger.info("[STARTUP] ✓ Complete")
    return True
