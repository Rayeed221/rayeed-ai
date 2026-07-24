"""
Navigation workflow — sequence:
  1. set_speed      (non-critical — warn and continue on failure)
  2. set_yaw        (optional)
  3. goto_position
  4. wait_arrival   (on failure, re-read position and retry once)

The planner's decision engine (safety gates + avoidance) governs in-flight
decisions separately.
"""

import logging

logger = logging.getLogger(__name__)


async def run_navigation(
    dispatcher, sm, safety, planner,
    lat: float, lon: float, alt: float,
    speed_ms: float = 5.0,
    yaw_deg:  float = None,
) -> bool:
    logger.info(f"[NAV] Navigating to ({lat:.6f}, {lon:.6f}, {alt}m) @ {speed_ms} m/s")

    # ── Step 1: Set speed (non-critical — warn and continue on failure) ───────
    resp = await dispatcher.dispatch("set_speed", {"speed_ms": speed_ms})
    if not resp.ok:
        logger.warning(f"[NAV] set_speed failed: {resp.error} — continuing")

    # ── Step 2: Set yaw (optional) ────────────────────────────────────────────
    if yaw_deg is not None:
        resp = await dispatcher.dispatch("set_yaw", {"yaw_deg": yaw_deg})
        if not resp.ok:
            logger.warning(f"[NAV] set_yaw failed: {resp.error} — continuing")

    # ── Step 3: Goto position ─────────────────────────────────────────────────
    resp = await dispatcher.dispatch("goto_position", {"lat": lat, "lon": lon, "alt": alt})
    if not resp.ok:
        logger.error(f"[NAV] goto_position failed: {resp.error}")
        return False

    # ── Step 4: Wait arrival (retry once on failure) ──────────────────────────
    resp = await dispatcher.dispatch("wait_arrival", {})
    if not resp.ok:
        logger.warning("[NAV] Arrival uncertain — re-reading position and retrying")
        pos = await dispatcher.dispatch("get_position_str", {})
        logger.info(f"[NAV] Current: {pos.data.get('position')}")

        resp = await dispatcher.dispatch("wait_arrival", {})
        if not resp.ok:
            logger.error("[NAV] Arrival confirmation failed after retry")
            return False

    logger.info("[NAV] ✓ Arrived at target")
    return True
