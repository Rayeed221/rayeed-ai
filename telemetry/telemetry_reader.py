import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TelemetryReader:
    """
    Periodically polls get_telemetry and updates the safety policy monitors.
    Runs as an independent asyncio task — never blocks audio or planner.

    If a PoseCache is provided it is updated with altitude and heading on
    every successful poll, enabling the localization system to track the
    drone's orientation for coordinate frame transforms.
    """

    def __init__(self, dispatcher, safety_policy, pose_cache=None, interval: float = 2.0):
        self._dispatcher = dispatcher
        self._safety     = safety_policy
        self._pose_cache = pose_cache   # Optional[PoseCache]
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
                    if self._pose_cache is not None:
                        self._pose_cache.update_telemetry(
                            alt_m=resp.data.get("altitude", 0.0),
                            heading_deg=resp.data.get("heading", 0.0),
                        )
                else:
                    logger.warning(f"[TELEMETRY] Poll failed: {resp.error}")
            except Exception as exc:
                logger.warning(f"[TELEMETRY] Exception: {exc}")
            await asyncio.sleep(self._interval)

    def latest(self) -> dict:
        return dict(self._latest)
