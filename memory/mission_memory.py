"""
Mission memory — persistent JSON storage (Decision 6B).
Supports:
  - Mission state recovery after crash/restart
  - Event log replay
  - Session history
"""

import json
import os
import time
import logging

from config import MEMORY_DIR, STATE_FILE
from schemas import MissionEvent

logger = logging.getLogger(__name__)


class MissionMemory:
    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self._state_path = os.path.join(MEMORY_DIR, STATE_FILE)
        self._log_path   = os.path.join(MEMORY_DIR, "mission_log.jsonl")
        self._state      = self._load_state()

    # ── Persistence ───────────────────────────────────────────────────────────

    def _load_state(self) -> dict:
        if os.path.exists(self._state_path):
            try:
                with open(self._state_path, "r") as f:
                    data = json.load(f)
                logger.info(f"[MEMORY] Restored state: {data.get('mission_state', 'unknown')}")
                return data
            except Exception as exc:
                logger.warning(f"[MEMORY] Failed to load state file: {exc}")
        return {
            "mission_state":  "idle",
            "last_position":  {},
            "last_telemetry": {},
            "session_start":  time.time(),
        }

    def save_state(self, updates: dict):
        self._state.update(updates)
        self._state["last_updated"] = time.time()
        try:
            with open(self._state_path, "w") as f:
                json.dump(self._state, f, indent=2)
        except Exception as exc:
            logger.error(f"[MEMORY] Failed to save state: {exc}")

    def log_event(self, event: MissionEvent):
        try:
            with open(self._log_path, "a") as f:
                f.write(json.dumps(event.to_dict()) + "\n")
        except Exception as exc:
            logger.error(f"[MEMORY] Failed to log event: {exc}")

    # ── Accessors ─────────────────────────────────────────────────────────────

    def get(self, key: str, default=None):
        return self._state.get(key, default)

    def all(self) -> dict:
        return dict(self._state)

    def clear(self):
        self._state = {"mission_state": "idle", "session_start": time.time()}
        self.save_state(self._state)
        logger.info("[MEMORY] State cleared")
