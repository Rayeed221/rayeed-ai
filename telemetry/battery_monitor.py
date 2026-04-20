import asyncio
import logging

from config import BATTERY_CRITICAL_PCT, BATTERY_LOW_PCT

logger = logging.getLogger(__name__)


class BatteryMonitor:
    """
    Reads battery percentage from adapter.snapshot() (populated by the streaming
    reader). No dispatcher call — just checks the cache.

    - LOW  → log warning, update safety policy
    - CRITICAL → trigger planner failsafe immediately (Decision 7C)
    """

    def __init__(self, adapter, safety_policy, planner, interval: float = 2.0):
        self._adapter   = adapter
        self._safety    = safety_policy
        self._planner   = planner
        self._interval  = interval
        self._last_warn = None

    async def run(self):
        while True:
            try:
                snap = self._adapter.snapshot()
                pct = snap.get("battery_pct")
                if pct is not None:
                    self._safety.update_battery(pct)
                    if pct <= BATTERY_CRITICAL_PCT:
                        logger.critical(f"[BATTERY] ⚠ CRITICAL: {pct:.1f}%")
                        await self._planner.trigger_failsafe(
                            reason=f"Battery critical at {pct:.1f}%"
                        )
                    elif pct <= BATTERY_LOW_PCT and self._last_warn != "low":
                        logger.warning(f"[BATTERY] LOW: {pct:.1f}%")
                        self._last_warn = "low"
                    elif pct > BATTERY_LOW_PCT:
                        self._last_warn = None
            except Exception as exc:
                logger.warning(f"[BATTERY] Exception: {exc}")
            await asyncio.sleep(self._interval)
