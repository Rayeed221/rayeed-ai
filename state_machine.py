from enum import Enum
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)


class MissionState(str, Enum):
    IDLE      = "idle"
    CONNECTED = "connected"
    ARMED     = "armed"
    TAKEOFF   = "takeoff"
    ENROUTE   = "enroute"
    HOVER     = "hover"
    LANDING   = "landing"
    RTL       = "rtl"
    FAILSAFE  = "failsafe"


# Only the state machine may change mission state — no direct assignment elsewhere.
LEGAL_TRANSITIONS: Dict[MissionState, Set[MissionState]] = {
    MissionState.IDLE:      {MissionState.CONNECTED, MissionState.FAILSAFE},
    MissionState.CONNECTED: {MissionState.ARMED, MissionState.IDLE, MissionState.FAILSAFE},
    MissionState.ARMED:     {MissionState.TAKEOFF, MissionState.CONNECTED, MissionState.FAILSAFE},
    MissionState.TAKEOFF:   {MissionState.HOVER, MissionState.ENROUTE, MissionState.FAILSAFE},
    MissionState.ENROUTE:   {MissionState.HOVER, MissionState.LANDING, MissionState.RTL, MissionState.FAILSAFE},
    MissionState.HOVER:     {MissionState.ENROUTE, MissionState.LANDING, MissionState.RTL, MissionState.FAILSAFE},
    MissionState.LANDING:   {MissionState.IDLE, MissionState.FAILSAFE},
    MissionState.RTL:       {MissionState.LANDING, MissionState.FAILSAFE},
    MissionState.FAILSAFE:  {MissionState.IDLE},
}


class IllegalTransitionError(Exception):
    pass


class StateMachine:
    def __init__(self):
        self._state   = MissionState.IDLE
        self._history: list = []

    @property
    def state(self) -> MissionState:
        return self._state

    def transition(self, new_state: MissionState) -> MissionState:
        """Hard transition — raises IllegalTransitionError on illegal move."""
        allowed = LEGAL_TRANSITIONS.get(self._state, set())
        if new_state not in allowed:
            raise IllegalTransitionError(
                f"Illegal transition: {self._state.value} → {new_state.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        logger.info(f"[STATE] {self._state.value} → {new_state.value}")
        self._history.append((self._state, new_state))
        self._state = new_state
        return self._state

    def force_failsafe(self) -> MissionState:
        """Bypass normal rules — always allowed from any state."""
        logger.warning(f"[STATE] FORCE FAILSAFE from {self._state.value}")
        self._history.append((self._state, MissionState.FAILSAFE))
        self._state = MissionState.FAILSAFE
        return self._state

    def is_airborne(self) -> bool:
        return self._state in {
            MissionState.TAKEOFF, MissionState.ENROUTE,
            MissionState.HOVER, MissionState.RTL,
        }

    def history(self) -> list:
        return list(self._history)

    def to_dict(self) -> dict:
        return {
            "state":   self._state.value,
            "history": [(a.value, b.value) for a, b in self._history],
        }
