import asyncio
import logging

logger = logging.getLogger(__name__)


class TelemetryReader:
    """
    Periodically polls get_telemetry and updates the safety policy monitors.
    Runs as an independent asyncio task — never blocks audio or planner.
    """

    def __init__(self, dispatcher, safety_policy, interval: float = 2.0):
        self._dispatcher = dispatcher
        self._safety     = safety_policy
        self._interval   = interval
        self._latest:    dict = {}

    async def run(self):
        while True:
            try:
                resp = await self._dispatcher.dispatch("get_telemetry", {})
                if resp.ok:
                    self._latest = resp.data
                    self._safety.update_telemetry_timestamp()
                    self._safety.update_altitude(resp.data.get("altitude", 0.0))
                else:
                    logger.warning(f"[TELEMETRY] Poll failed: {resp.error}")
            except Exception as exc:
                logger.warning(f"[TELEMETRY] Exception: {exc}")
            await asyncio.sleep(self._interval)

    def latest(self) -> dict:
        return dict(self._latest)
