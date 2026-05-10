"""
workflows/takeoff_oracle.py — Oracle-guided takeoff workflow for DroneAI.

Replaces workflows/takeoff.py with sequential oracle deliberation between steps.

Sequence (each step is oracle-reviewed before advancing):
  1. set_mode(GUIDED)
  2. arm_drone
  3. takeoff(altitude)
  4. wait_altitude(altitude)

The oracle thinks between every step — even on success — because transitions
between CONNECTED → ARMED → TAKEOFF are the highest-risk state changes.
"""

import asyncio
import logging

from thinking_oracle import ThinkingOracle

logger = logging.getLogger(__name__)

_oracle = ThinkingOracle()


async def _oracle_step(
    dispatcher, planner, tool_name: str, args: dict, sm, safety,
    max_retries: int = 3,
) -> tuple[bool, dict]:
    """
    Execute one workflow step with oracle deliberation.

    Returns:
        (success: bool, result_data: dict)
    """
    for attempt in range(max_retries + 1):
        resp = await dispatcher.dispatch(tool_name, args)

        tel_age = (
            0.0 if safety._last_tel_time == 0.0
            else __import__("time").time() - safety._last_tel_time
        )
        ctx = {
            "tool":              tool_name,
            "ok":                resp.ok,
            "error":             resp.error,
            "state":             resp.state,
            "battery_pct":       safety._last_battery,
            "altitude_m":        safety._last_altitude,
            "telemetry_age_sec": tel_age,
            "retry_count":       attempt,
            "airborne":          sm.is_airborne(),
        }

        td = await asyncio.to_thread(_oracle.deliberate, ctx)

        logger.info(
            f"[TAKEOFF:ORACLE] {tool_name} attempt={attempt} "
            f"→ {td.decision} | {td.reason} | conf={td.confidence:.2f} "
            f"| {td.latency_ms:.0f}ms | src={td.source}"
        )
        logger.debug(f"[TAKEOFF:ORACLE:THINKING]\n{td.thinking[:500]}")

        if td.decision == "FAILSAFE":
            await planner.trigger_failsafe(reason=f"oracle[{tool_name}]: {td.reason}")
            return False, {}

        if td.decision == "ABORT":
            logger.error(f"[TAKEOFF] Oracle ABORT at {tool_name}: {td.reason}")
            return False, {}

        if td.decision == "WAIT":
            wait_s = td.wait_sec or 1.0
            logger.info(f"[TAKEOFF] Oracle WAIT {wait_s}s — {td.reason}")
            await asyncio.sleep(wait_s)
            # After wait, re-dispatch same step
            continue

        if td.decision == "RETRY" and attempt < max_retries:
            logger.warning(f"[TAKEOFF] Oracle RETRY {tool_name} (attempt {attempt + 1})")
            await asyncio.sleep(0.5 * (attempt + 1))  # exponential backoff
            continue

        # CONTINUE or REPLAN — treat as proceed
        if td.decision == "REPLAN":
            logger.warning(f"[TAKEOFF] Oracle REPLAN during {tool_name} — aborting takeoff")
            return False, {}

        return resp.ok, resp.data

    logger.error(f"[TAKEOFF] {tool_name} exceeded max retries")
    return False, {}


async def run_takeoff_oracle(
    dispatcher, sm, safety, planner,
    altitude: float = 10.0,
) -> bool:
    """
    Oracle-guided takeoff. Each step is deliberated individually.
    Drop-in replacement for workflows/takeoff.py run_takeoff().
    """
    logger.info(f"[TAKEOFF:ORACLE] Initiating oracle-guided takeoff to {altitude}m")

    steps = [
        ("set_mode",      {"mode": "GUIDED"}),
        ("arm_drone",     {}),
        ("takeoff",       {"altitude": altitude}),
        ("wait_altitude", {"target_alt": altitude}),
    ]

    for tool_name, args in steps:
        ok, data = await _oracle_step(dispatcher, planner, tool_name, args, sm, safety)
        if not ok:
            logger.error(f"[TAKEOFF:ORACLE] Failed at step: {tool_name}")
            return False
        logger.info(f"[TAKEOFF:ORACLE] ✓ {tool_name} — data={data}")

    logger.info(f"[TAKEOFF:ORACLE] ✓ Complete — hovering at {altitude}m")
    logger.info(f"[TAKEOFF:ORACLE] Oracle stats: {_oracle.stats()}")
    return True
