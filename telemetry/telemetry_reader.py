import asyncio
import logging

logger = logging.getLogger(__name__)


class TelemetryReader:
    """
    Pumps live values from adapter.snapshot() into the safety policy.
    Does NOT go through the dispatcher — the snapshot is already populated by
    the adapter's streaming reader, so there is no MAVLink roundtrip per tick.
    Runs as an independent asyncio task — never blocks audio or planner.
    """

    def __init__(self, adapter, safety_policy, interval: float = 0.5):
        self._adapter  = adapter
        self._safety   = safety_policy
        self._interval = interval
        self._latest:  dict = {}

    async def run(self):
        while True:
            try:
                snap = self._adapter.snapshot()
                if snap:
                    self._latest = snap
                    self._safety.update_telemetry_timestamp()
                    if "altitude" in snap:
                        self._safety.update_altitude(snap["altitude"])
            except Exception as exc:
                logger.warning(f"[TELEMETRY] Exception: {exc}")
            await asyncio.sleep(self._interval)

    def latest(self) -> dict:
        return dict(self._latest)
