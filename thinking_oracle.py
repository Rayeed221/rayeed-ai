"""
thinking_oracle.py — compatibility shim.

The oracle implementation lives in ``planner.py`` alongside the reflex tier
that decides when to invoke it.  This module used to carry a second, nearly
identical copy: the two drifted (only planner's had the ``_from_dict`` fix and
the latency tuning), and whichever one a caller happened to import decided how
much latency it paid.  Re-exporting keeps the old import paths working while
there is exactly one implementation to tune.

Prefer importing from ``planner`` in new code:

    from planner import ThinkingOracle, ThinkingDecision

Build the Ollama model first:
    ollama create droneoracle -f thinking_oracle.Modelfile
"""

from planner import (  # noqa: F401  (re-exported for backwards compatibility)
    HIGH_VALUE_TOOLS,
    ORACLE_MODEL,
    ORACLE_TIMEOUT,
    VALID_DECISIONS,
    ThinkingDecision,
    ThinkingOracle,
    build_oracle_context,
)

# Tools watched by the dispatcher post-execution hook (subset of HIGH_VALUE_TOOLS)
ORACLE_WATCHED_TOOLS = {
    "arm_drone", "takeoff", "goto_position",
    "return_to_launch", "land",
}

__all__ = [
    "HIGH_VALUE_TOOLS",
    "ORACLE_MODEL",
    "ORACLE_TIMEOUT",
    "ORACLE_WATCHED_TOOLS",
    "VALID_DECISIONS",
    "ThinkingDecision",
    "ThinkingOracle",
    "build_oracle_context",
]
