import asyncio
import logging

logger = logging.getLogger(__name__)


class PositionMonitor:
    """
    Periodically reads GPS position via get_position_str.
    Cached value available via .latest() for workflows and memory.
    Runs as an independent asyncio task.
    """

    def __init__(self, dispatcher, interval: float = 5.0):
        self._dispatcher = dispatcher
        self._interval   = interval
        self._latest:    dict = {}

    async def run(self):
        while True:
            try:
                resp = await self._dispatcher.dispatch("get_position_str", {})
                if resp.ok:
                    self._latest = resp.data
                    logger.debug(f"[POSITION] {resp.data.get('position')}")
                else:
                    logger.warning(f"[POSITION] Poll failed: {resp.error}")
            except Exception as exc:
                logger.warning(f"[POSITION] Exception: {exc}")
            await asyncio.sleep(self._interval)

    def latest(self) -> dict:
        return dict(self._latest)
