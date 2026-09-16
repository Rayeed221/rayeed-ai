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

    # ── Wire format ──────────────────────────────────────────────────────

    def to_llm(self) -> dict:
        """
        Compact form sent back to the Live model.

        Every tool result is re-tokenised by the model before it can speak, so
        fields it never reads are pure latency.  Dropped: the epoch timestamp,
        and any field still at its default (error/next_action/wait = None,
        confidence = 1.0).  Nothing the model reasons over is removed — `data`
        is passed through untouched.

        Typical saving is ~35 tokens per tool call, and it compounds because
        the Live session keeps the whole exchange in context.
        """
        out = {"ok": self.ok, "tool": self.tool, "state": self.state}
        if self.data:
            out["data"] = self.data
        if self.error is not None:
            out["error"] = self.error
        if self.next_action is not None:
            out["next_action"] = self.next_action
        if self.wait is not None:
            out["wait"] = self.wait.to_dict()
        if self.confidence != 1.0:
            out["confidence"] = self.confidence
        return out

    def sentence(self) -> str:
        """
        One-line symbolic form for logs and mission memory:
            ``OK takeoff | hover | next=wait_altitude``
            ``ERR goto_position | enroute | AVOIDANCE_ACTIVE ...``
        Compact, greppable, and cheap to emit at 20 Hz.
        """
        head = "OK" if self.ok else "ERR"
        parts = [f"{head} {self.tool}", self.state]
        if self.error:
            parts.append(self.error[:60])
        if self.next_action:
            parts.append(f"next={self.next_action}")
        if self.wait:
            parts.append(f"wait={self.wait.seconds}s")
        return " | ".join(parts)

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
