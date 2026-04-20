"""
Intent-verb registry — maps LLM tool names to workflow coroutines.

When the LLM calls one of these tool names, app.py's router intercepts the
call and runs the full workflow instead of dispatching the adapter primitive.
This turns takeoff / goto_position / land / return_to_launch into atomic verbs
that internally compose set_mode, arm, wait, etc.

New intents added for compactness:
  - hold_position(seconds, yaw_deg?) → run_inspection
  - emergency_stop(reason?)          → planner.trigger_failsafe (handled in app.py)
"""

from dataclasses import dataclass
from typing import Callable, Dict, Any

from workflows.takeoff     import run_takeoff
from workflows.navigation  import run_navigation
from workflows.landing     import run_landing
from workflows.return_home import run_return_home
from workflows.inspection  import run_inspection


@dataclass
class IntentSpec:
    fn:      Callable
    arg_map: Dict[str, str]   # {llm_arg_name: workflow_kwarg_name}


WORKFLOW_INTENTS: Dict[str, IntentSpec] = {
    "takeoff": IntentSpec(
        fn=run_takeoff,
        arg_map={"altitude": "altitude"},
    ),
    "goto_position": IntentSpec(
        fn=run_navigation,
        arg_map={
            "lat":      "lat",
            "lon":      "lon",
            "alt":      "alt",
            "speed_ms": "speed_ms",
            "yaw_deg":  "yaw_deg",
        },
    ),
    "land": IntentSpec(
        fn=run_landing,
        arg_map={},
    ),
    "return_to_launch": IntentSpec(
        fn=run_return_home,
        arg_map={},
    ),
    "hold_position": IntentSpec(
        fn=run_inspection,
        arg_map={
            "seconds": "hold_seconds",
            "yaw_deg": "yaw_deg",
        },
    ),
}


def is_intent(name: str) -> bool:
    return name in WORKFLOW_INTENTS


def resolve_kwargs(name: str, llm_args: Dict[str, Any]) -> Dict[str, Any]:
    """Map LLM-supplied args → workflow kwargs. Drops unknown keys and omits
    None so the workflow's defaults apply."""
    spec = WORKFLOW_INTENTS[name]
    return {
        spec.arg_map[k]: v
        for k, v in llm_args.items()
        if k in spec.arg_map and v is not None
    }
