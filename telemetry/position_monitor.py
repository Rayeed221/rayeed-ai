import asyncio
import logging
import re

logger = logging.getLogger(__name__)

# Matches the position string returned by get_position_str(), e.g.:
# "Lat: 23.810300, Lon: 90.412500, Alt: 5.0m"
_POS_RE = re.compile(
    r"Lat:\s*([-\d.]+),\s*Lon:\s*([-\d.]+),\s*Alt:\s*([\d.]+)m",
    re.IGNORECASE,
)


class PositionMonitor:
    """
    Periodically reads GPS position via get_position_str.
    Cached value available via .latest() for workflows and memory.
    Runs as an independent asyncio task.

    If a PoseCache is provided, the parsed lat/lon/alt are fed into it on
    every successful poll so the localization system has GPS coordinates
    for NED → global frame transforms.
    """

    def __init__(self, dispatcher, pose_cache=None, interval: float = 5.0):
        self._dispatcher = dispatcher
        self._pose_cache = pose_cache   # Optional[PoseCache]
        self._interval   = interval
        self._latest:    dict = {}

    async def run(self):
        while True:
            try:
                resp = await self._dispatcher.dispatch("get_position_str", {})
                if resp.ok:
                    self._latest = resp.data
                    pos_str = resp.data.get("position", "")
                    logger.debug(f"[POSITION] {pos_str}")
                    if self._pose_cache is not None:
                        m = _POS_RE.match(pos_str)
                        if m:
                            self._pose_cache.update_position(
                                lat=float(m.group(1)),
                                lon=float(m.group(2)),
                                alt_m=float(m.group(3)),
                            )
                else:
                    logger.warning(f"[POSITION] Poll failed: {resp.error}")
            except Exception as exc:
                logger.warning(f"[POSITION] Exception: {exc}")
            await asyncio.sleep(self._interval)

    def latest(self) -> dict:
        return dict(self._latest)
