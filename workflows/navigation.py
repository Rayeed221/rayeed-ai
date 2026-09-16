"""
Navigation workflow — sequence:
  1. set_speed
  2. set_yaw  (optional)
  3. goto_position  ← oracle mandatory
  4. wait_arrival   ← oracle confirms arrival is nominal

The planner's reflex tier checks each critical step; the oracle is consulted
only when an outcome cannot be classified deterministically.  On ABORT/REPLAN
at arrival, re-reads position and retries once with a re-check.
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def _deliberate(planner, tool_name: str, resp) -> object:
    """Reflex-first step decision (falls through to the oracle if ambiguous)."""
    td = await planner.deliberate_step(resp)
    logger.info(
        f"[NAV] {tool_name} → {td.decision} | {td.reason} "
        f"| conf={td.confidence:.2f} | {td.latency_ms:.0f}ms | src={td.source}"
    )
    logger.debug(f"[NAV:THINKING]\n{td.thinking[:400]}")
    return td


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
        td   = await _deliberate(planner, "set_yaw", resp)
        if td.decision == "FAILSAFE":
            await planner.trigger_failsafe(reason=f"oracle[set_yaw]: {td.reason}")
            return False
        if td.wait_sec:
            await asyncio.sleep(td.wait_sec)

    # ── Step 3: Goto position (oracle mandatory) ──────────────────────────────
    resp = await dispatcher.dispatch("goto_position", {"lat": lat, "lon": lon, "alt": alt})
    td   = await _deliberate(planner, "goto_position", resp)

    if td.decision == "FAILSAFE":
        await planner.trigger_failsafe(reason=f"oracle[goto_position]: {td.reason}")
        return False

    if td.decision in ("ABORT", "REPLAN"):
        logger.error(f"[NAV] {td.decision} at goto_position: {td.reason}")
        return False

    if td.decision == "WAIT":
        wait_s = td.wait_sec or 1.0
        logger.info(f"[NAV] Post-goto WAIT {wait_s}s — {td.reason}")
        await asyncio.sleep(wait_s)

    # ── Step 4: Wait arrival with oracle confirmation ─────────────────────────
    resp = await dispatcher.dispatch("wait_arrival", {})
    td   = await _deliberate(planner, "wait_arrival", resp)

    if td.decision == "FAILSAFE":
        await planner.trigger_failsafe(reason=f"oracle[wait_arrival]: {td.reason}")
        return False

    if not resp.ok or td.decision in ("ABORT", "REPLAN"):
        logger.warning("[NAV] Arrival uncertain — re-reading position")
        pos = await dispatcher.dispatch("get_position_str", {})
        logger.info(f"[NAV] Current: {pos.data.get('position')}")

        resp = await dispatcher.dispatch("wait_arrival", {})
        td   = await _deliberate(planner, "wait_arrival (retry)", resp)
        if not resp.ok:
            logger.error("[NAV] Arrival confirmation failed after retry")
            return False

    logger.info("[NAV] ✓ Arrived at target")
    logger.info(f"[NAV] Decision tiers: {planner.decision_stats()}")
    return True
