"""
tests/test_drone/test_dispatch_timeouts.py — per-tool execution deadlines.

One 10 s budget for every tool meant the blocking wait_* tools could never
succeed: the adapter waits up to 60 s for altitude and 120 s for arrival, so
the dispatcher cut them off at 10 s, reported next_action="retry", and burned a
retry plus an LLM round trip on every takeoff.
"""

import asyncio
import time

import pytest

from config import MAVLINK_WAIT_ALTITUDE_SEC, MAVLINK_WAIT_ARRIVAL_SEC
from safety_policy import SafetyPolicy
from state_machine import StateMachine, MissionState
import tool_dispatcher
from tool_dispatcher import (
    TOOL_TIMEOUT_SEC,
    ToolDispatcher,
    timeout_for,
)


# ── timeout_for ───────────────────────────────────────────────────────────────

def test_default_timeout_unchanged_for_normal_tools():
    assert timeout_for("get_telemetry", {}) == TOOL_TIMEOUT_SEC
    assert timeout_for("arm_drone", {}) == TOOL_TIMEOUT_SEC
    assert timeout_for("goto_position", {"lat": 1, "lon": 2, "alt": 3}) == TOOL_TIMEOUT_SEC


def test_wait_tools_get_budgets_matching_the_adapter():
    assert timeout_for("wait_altitude", {}) > MAVLINK_WAIT_ALTITUDE_SEC
    assert timeout_for("wait_arrival", {}) > MAVLINK_WAIT_ARRIVAL_SEC


def test_wait_time_budget_follows_its_argument():
    assert timeout_for("wait_time", {"seconds": 30}) > 30
    assert timeout_for("wait_time", {"seconds": 0.5}) > 0.5


def test_wait_time_handles_bad_arguments():
    assert timeout_for("wait_time", {}) == 5.0
    assert timeout_for("wait_time", {"seconds": "soon"}) == TOOL_TIMEOUT_SEC


def test_connect_outlasts_the_heartbeat_wait():
    # MAVLinkAdapter._handle_connect_drone uses wait_heartbeat(timeout=15)
    assert timeout_for("connect_drone", {}) > 15.0


# ── End-to-end through the dispatcher ─────────────────────────────────────────

class SlowAdapter:
    """Blocks for `delay` seconds, like a real wait_* handler would."""

    def __init__(self, delay: float):
        self._delay = delay

    def execute(self, tool_name, args):
        time.sleep(self._delay)
        return {"status": "altitude_reached", "altitude": 10.0}


@pytest.fixture
def parts():
    sm = StateMachine()
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    safety = SafetyPolicy(sm)
    return sm, safety


@pytest.mark.asyncio
async def test_slow_wait_tool_is_not_cut_off_at_the_default_budget(parts):
    """A wait_altitude that takes longer than 10 s must still be allowed to
    finish — under the old uniform budget it was guaranteed to fail."""
    sm, safety = parts
    dispatcher = ToolDispatcher(sm, safety, SlowAdapter(delay=0.2))

    resp = await dispatcher.dispatch("wait_altitude", {"target_alt": 10.0})

    assert resp.ok is True
    assert resp.data["status"] == "altitude_reached"
    assert safety.check_retry_limit("wait_altitude") is None   # no retry burned


@pytest.mark.asyncio
async def test_timeout_still_fires_and_reports_its_budget(parts, monkeypatch):
    sm, safety = parts
    monkeypatch.setitem(tool_dispatcher.TOOL_TIMEOUTS, "wait_altitude", 0.05)
    dispatcher = ToolDispatcher(sm, safety, SlowAdapter(delay=1.0))

    t0 = time.monotonic()
    resp = await dispatcher.dispatch("wait_altitude", {"target_alt": 10.0})
    elapsed = time.monotonic() - t0

    assert resp.ok is False
    assert "timed out after 0.05s" in resp.error
    assert resp.next_action == "retry"
    assert elapsed < 2.0
