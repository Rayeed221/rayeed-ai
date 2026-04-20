import asyncio
import logging

logger = logging.getLogger(__name__)


class PositionMonitor:
    """
    Caches the latest GPS position from adapter.snapshot() for workflows and
    memory. No dispatcher call — reads directly from the streamer cache.
    """

    def __init__(self, adapter, interval: float = 1.0):
        self._adapter  = adapter
        self._interval = interval
        self._latest:  dict = {}

    async def run(self):
        while True:
            try:
                snap = self._adapter.snapshot()
                if "lat" in snap:
                    self._latest = {
                        "lat":      snap["lat"],
                        "lon":      snap["lon"],
                        "altitude": snap.get("altitude", 0.0),
                        "heading":  snap.get("heading", 0.0),
                    }
            except Exception as exc:
                logger.warning(f"[POSITION] Exception: {exc}")
            await asyncio.sleep(self._interval)

    def latest(self) -> dict:
        return dict(self._latest)
