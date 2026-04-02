"""
Environment memory — persists spatial knowledge across sessions.
Stores: named waypoints, obstacle markers, no-fly zones.
"""

import json
import os
import time
import logging

from config import MEMORY_DIR

logger = logging.getLogger(__name__)
_ENV_FILE = os.path.join(MEMORY_DIR, "environment.json")


class EnvironmentMemory:
    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(_ENV_FILE):
            try:
                with open(_ENV_FILE, "r") as f:
                    return json.load(f)
            except Exception as exc:
                logger.warning(f"[ENV_MEM] Load failed: {exc}")
        return {"waypoints": {}, "obstacles": [], "no_fly_zones": []}

    def _save(self):
        try:
            with open(_ENV_FILE, "w") as f:
                json.dump(self._data, f, indent=2)
        except Exception as exc:
            logger.error(f"[ENV_MEM] Save failed: {exc}")

    # ── Waypoints ─────────────────────────────────────────────────────────────

    def add_waypoint(self, name: str, lat: float, lon: float, alt: float):
        self._data["waypoints"][name] = {
            "lat": lat, "lon": lon, "alt": alt, "added": time.time()
        }
        self._save()
        logger.info(f"[ENV_MEM] Waypoint saved: '{name}' ({lat}, {lon}, {alt}m)")

    def get_waypoint(self, name: str) -> dict | None:
        return self._data["waypoints"].get(name)

    def all_waypoints(self) -> dict:
        return dict(self._data["waypoints"])

    def remove_waypoint(self, name: str):
        self._data["waypoints"].pop(name, None)
        self._save()

    # ── Obstacles ─────────────────────────────────────────────────────────────

    def add_obstacle(self, lat: float, lon: float, radius_m: float, description: str = ""):
        self._data["obstacles"].append({
            "lat": lat, "lon": lon,
            "radius_m": radius_m,
            "description": description,
            "added": time.time(),
        })
        self._save()

    def clear_obstacles(self):
        self._data["obstacles"] = []
        self._save()

    def obstacles(self) -> list:
        return list(self._data["obstacles"])

    # ── No-fly zones ──────────────────────────────────────────────────────────

    def add_no_fly_zone(self, lat: float, lon: float, radius_m: float, label: str = ""):
        self._data["no_fly_zones"].append({
            "lat": lat, "lon": lon,
            "radius_m": radius_m,
            "label": label,
            "added": time.time(),
        })
        self._save()

    def no_fly_zones(self) -> list:
        return list(self._data["no_fly_zones"])
