"""
tests/test_drone/test_dispatch_timeouts.py — per-tool execution deadlines.

One 10 s budget for every tool meant the blocking wait_* tools could never
succeed: the MAVLink adapter waits up to 60 s for altitude and 120 s for
arrival, so the dispatcher cut them off at 10 s, reported next_action="retry",
and burned a retry plus an LLM round trip on every takeoff.

The budget belongs to the backend, not the tool — only the code that does the
waiting knows how long its wait can take. SimAdapter answers from memory and
keeps the default.
"""

import time

import pytest

from adapters.base_adapter import DEFAULT_TOOL_TIMEOUT_SEC
from adapters.mavlink_adapter import MAVLinkAdapter
from adapters.sim_adapter import SimAdapter
from config import MAVLINK_WAIT_ALTITUDE_SEC, MAVLINK_WAIT_ARRIVAL_SEC
from safety_policy import SafetyPolicy
from state_machine import StateMachine, MissionState
from tool_dispatcher import ToolDispatcher


@pytest.fixture
def mav():
    return MAVLinkAdapter("udp:127.0.0.1:14550")


@pytest.fixture
def sim():
    return SimAdapter()


# ── Backend-owned budgets ─────────────────────────────────────────────────────

def test_default_budget_for_tools_that_do_not_wait(mav):
    assert mav.timeout_for("get_telemetry", {}) == DEFAULT_TOOL_TIMEOUT_SEC
    assert mav.timeout_for("arm_drone", {}) == DEFAULT_TOOL_TIMEOUT_SEC
    assert mav.timeout_for("goto_position", {"lat": 1, "lon": 2, "alt": 3}) == DEFAULT_TOOL_TIMEOUT_SEC


def test_mavlink_wait_tools_outlast_their_own_deadlines(mav):
    assert mav.timeout_for("wait_altitude", {}) > MAVLINK_WAIT_ALTITUDE_SEC
    assert mav.timeout_for("wait_arrival", {}) > MAVLINK_WAIT_ARRIVAL_SEC


def test_mavlink_connect_outlasts_its_heartbeat_wait(mav):
    # _handle_connect_drone blocks in wait_heartbeat(timeout=_HEARTBEAT_WAIT_SEC)
    from adapters.mavlink_adapter import _HEARTBEAT_WAIT_SEC
    assert mav.timeout_for("connect_drone", {}) > _HEARTBEAT_WAIT_SEC


def test_mavlink_wait_time_budget_follows_its_argument(mav):
    assert mav.timeout_for("wait_time", {"seconds": 30}) > 30
    assert mav.timeout_for("wait_time", {"seconds": 0.5}) > 0.5


def test_mavlink_wait_time_handles_bad_arguments(mav):
    assert mav.timeout_for("wait_time", {}) == 5.0
    assert mav.timeout_for("wait_time", {"seconds": "soon"}) == DEFAULT_TOOL_TIMEOUT_SEC


def test_sim_keeps_the_default_for_everything(sim):
    """SimAdapter returns instantly, so a 125 s arrival budget would describe
    hardware it is not talking to."""
    for tool, args in [
        ("get_telemetry", {}),
        ("connect_drone", {}),
        ("wait_altitude", {"target_alt": 5.0}),
        ("wait_arrival", {}),
        ("wait_time", {"seconds": 30}),
    ]:
        assert sim.timeout_for(tool, args) == DEFAULT_TOOL_TIMEOUT_SEC


# ── End-to-end through the dispatcher ─────────────────────────────────────────

class SlowAdapter(SimAdapter):
    """Blocks for `delay` seconds, and claims a budget that allows it."""

    def __init__(self, delay: float, budget: float = 60.0):
        super().__init__()
        self._delay  = delay
        self._budget = budget

    def execute(self, tool_name, args):
        time.sleep(self._delay)
        return {"status": "altitude_reached", "altitude": 10.0}

    def timeout_for(self, tool_name, args):
        return self._budget


@pytest.fixture
def parts():
    sm = StateMachine()
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    return sm, SafetyPolicy(sm)


@pytest.mark.asyncio
async def test_slow_wait_tool_is_not_cut_off_at_the_default_budget(parts):
    """A wait_altitude that takes longer than the default must still be allowed
    to finish — under the old uniform budget it was guaranteed to fail."""
    sm, safety = parts
    dispatcher = ToolDispatcher(sm, safety, SlowAdapter(delay=0.2, budget=60.0))

    resp = await dispatcher.dispatch("wait_altitude", {"target_alt": 10.0})

    assert resp.ok is True
    assert resp.data["status"] == "altitude_reached"
    assert safety.check_retry_limit("wait_altitude") is None   # no retry burned


@pytest.mark.asyncio
async def test_timeout_still_fires_and_reports_the_backend_budget(parts):
    sm, safety = parts
    dispatcher = ToolDispatcher(sm, safety, SlowAdapter(delay=1.0, budget=0.05))

    t0 = time.monotonic()
    resp = await dispatcher.dispatch("wait_altitude", {"target_alt": 10.0})
    elapsed = time.monotonic() - t0

    assert resp.ok is False
    assert "timed out after 0.05s" in resp.error
    assert resp.next_action == "retry"
    assert elapsed < 2.0
