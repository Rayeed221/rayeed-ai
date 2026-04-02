import logging

logger = logging.getLogger(__name__)


class TurnManager:
    """
    Controls microphone gating during AI speech and tool execution.

    Rules:
      - block()   → mic is silenced (AI speaking or critical action executing)
      - unblock() → mic is re-enabled (playback queue drained, turn complete)
      - Audio playback and telemetry tasks run regardless of block state.
      - Planner wait periods do NOT block the mic — only AI speech does.
    """

    def __init__(self):
        self._blocked = False

    def block(self):
        if not self._blocked:
            self._blocked = True
            logger.debug("[TURN] Mic blocked")

    def unblock(self):
        if self._blocked:
            self._blocked = False
            logger.info("[TURN] Mic unblocked — listening...")

    def is_blocked(self) -> bool:
        return self._blocked
