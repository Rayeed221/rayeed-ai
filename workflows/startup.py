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
        # Honour any active wait before the next step
        while planner.is_waiting():
            await asyncio.sleep(0.2)

        resp = await dispatcher.dispatch(tool_name, arg_fn(connection_string))
        logger.info(f"[STARTUP] {tool_name} → ok={resp.ok} state={resp.state}")

        if not resp.ok:
            logger.error(f"[STARTUP] Failed at '{tool_name}': {resp.error}")
            return False

        if resp.wait:
            planner.schedule_wait(resp.wait)
            while planner.is_waiting():
                await asyncio.sleep(0.2)

    logger.info("[STARTUP] ✓ Complete")
    return True
