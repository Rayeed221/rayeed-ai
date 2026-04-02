import asyncio
import logging

from config import BATTERY_CRITICAL_PCT, BATTERY_LOW_PCT

logger = logging.getLogger(__name__)


class BatteryMonitor:
    """
    Periodically checks battery via get_battery.
    - LOW  → log warning, update safety policy
    - CRITICAL → trigger planner failsafe immediately (Decision 7C)

    Runs as an independent asyncio task.
    """

    def __init__(self, dispatcher, safety_policy, planner, interval: float = 10.0):
        self._dispatcher = dispatcher
        self._safety     = safety_policy
        self._planner    = planner
        self._interval   = interval

    async def run(self):
        while True:
            try:
                resp = await self._dispatcher.dispatch("get_battery", {})
                if resp.ok:
                    pct = resp.data.get("level_percent", 100.0)
                    self._safety.update_battery(pct)

                    if pct <= BATTERY_CRITICAL_PCT:
                        logger.critical(f"[BATTERY] ⚠ CRITICAL: {pct:.1f}%")
                        await self._planner.trigger_failsafe(
                            reason=f"Battery critical at {pct:.1f}%"
                        )
                    elif pct <= BATTERY_LOW_PCT:
                        logger.warning(f"[BATTERY] LOW: {pct:.1f}%")
                else:
                    logger.warning(f"[BATTERY] Poll failed: {resp.error}")
            except Exception as exc:
                logger.warning(f"[BATTERY] Exception: {exc}")
            await asyncio.sleep(self._interval)
