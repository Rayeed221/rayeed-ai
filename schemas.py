"""
Standard response schema used by every tool, workflow, and dispatcher.

Shape:
{
    "ok":          bool,
    "tool":        str,
    "state":       str,
    "data":        dict,
    "error":       str | None,
    "next_action": str | None,
    "wait":        {"seconds": float, "reason": str} | None,
    "confidence":  float,
    "timestamp":   float,
}
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import time


@dataclass
class WaitInstruction:
    seconds: float
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ToolResponse:
    ok:          bool
    tool:        str
    state:       str
    data:        dict                    = field(default_factory=dict)
    error:       Optional[str]          = None
    next_action: Optional[str]          = None
    wait:        Optional[WaitInstruction] = None
    confidence:  float                  = 1.0
    timestamp:   float                  = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return asdict(self)

    # ── Factories ────────────────────────────────────────────────────────

    @staticmethod
    def success(
        tool:        str,
        state:       str,
        data:        dict = None,
        next_action: str  = None,
        wait:        WaitInstruction = None,
        confidence:  float = 1.0,
    ) -> "ToolResponse":
        return ToolResponse(
            ok=True, tool=tool, state=state,
            data=data or {}, next_action=next_action,
            wait=wait, confidence=confidence,
        )

    @staticmethod
    def failure(
        tool:        str,
        state:       str,
        error:       str,
        next_action: str   = None,
        confidence:  float = 0.0,
    ) -> "ToolResponse":
        return ToolResponse(
            ok=False, tool=tool, state=state,
            error=error, next_action=next_action,
            confidence=confidence,
        )


@dataclass
class MissionEvent:
    event_type: str          # "tool_call" | "state_change" | "error" | "plan_decision"
    tool:       Optional[str]
    state:      str
    detail:     dict         = field(default_factory=dict)
    timestamp:  float        = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ErrorSchema:
    code:      str
    message:   str
    retryable: bool
    context:   dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)
