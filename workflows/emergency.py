"""
Emergency workflow — triggered by:
  - Battery critical
  - Telemetry stale beyond emergency threshold
  - Repeated tool failures (MAX_RETRIES)
  - Geofence breach
  - Mission timeout
  - Any planner FAILSAFE decision

Sequence:
  1. Stop current plan (planner already in FAILSAFE)
  2. Try set_mode(RTL) with short timeout
  3. Try land (fallback if RTL fails)
  4. Wait for ground contact
  5. Disarm
"""

import asyncio
import logging

logger = logging.getLogger(__name__)

_SHORT_TIMEOUT = 5.0
_GROUND_WAIT   = 3.0


async def _try(coro, label: str):
    """Attempt a coroutine with a short timeout — log but never raise."""
    try:
        return await asyncio.wait_for(coro, timeout=_SHORT_TIMEOUT)
    except asyncio.TimeoutError:
        logger.critical(f"[EMERGENCY] {label} timed out")
    except Exception as exc:
        logger.critical(f"[EMERGENCY] {label} exception: {exc}")
    return None


async def run_emergency(dispatcher, sm, safety, planner, reason: str = "unknown") -> bool:
    logger.critical(f"[EMERGENCY] ⚠ Triggered — reason: {reason}")

    # Step 1: Attempt RTL mode
    rtl_resp = await _try(
        dispatcher.dispatch("set_mode", {"mode": "RTL"}),
        "set_mode(RTL)",
    )
    if rtl_resp and rtl_resp.ok:
        logger.info("[EMERGENCY] RTL mode set — waiting for descent")
        await asyncio.sleep(_GROUND_WAIT)

    # Step 2: Force land regardless
    await _try(dispatcher.dispatch("land", {}), "land")
    logger.info("[EMERGENCY] Land command issued")

    # Step 3: Wait for ground contact
    await asyncio.sleep(_GROUND_WAIT)

    # Step 4: Disarm
    disarm_resp = await _try(dispatcher.dispatch("disarm_drone", {}), "disarm_drone")
    if disarm_resp and disarm_resp.ok:
        logger.info("[EMERGENCY] Disarmed successfully")
    else:
        logger.critical("[EMERGENCY] Disarm failed — manual intervention required")

    logger.critical("[EMERGENCY] ✓ Emergency workflow complete")
    return True
