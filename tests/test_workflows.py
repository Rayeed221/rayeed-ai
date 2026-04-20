import pytest
import asyncio
from unittest.mock import AsyncMock

from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy
from planner import Planner


# ── Helpers ───────────────────────────────────────────────────────────────────

def ok(tool, state="connected", data=None, next_action=None, wait=None):
    return ToolResponse.success(tool=tool, state=state, data=data, next_action=next_action, wait=wait)

def fail(tool, state="idle", error="MOCK_ERROR", next_action=None):
    return ToolResponse.failure(tool=tool, state=state, error=error, next_action=next_action)


@pytest.fixture
def sm():
    return StateMachine()

@pytest.fixture
def safety(sm):
    return SafetyPolicy(sm)

@pytest.fixture
def dispatcher():
    d = AsyncMock()
    d.dispatch = AsyncMock(return_value=ok("test"))
    return d

@pytest.fixture
def planner(sm, safety, dispatcher):
    return Planner(sm, safety, dispatcher)


# ── Startup ───────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_startup_success(dispatcher, sm, safety, planner):
    from workflows.startup import run_startup
    dispatcher.dispatch.return_value = ok("connect_drone", state="connected")
    result = await run_startup(dispatcher, sm, safety, planner)
    assert result is True
    assert dispatcher.dispatch.call_count == 5


@pytest.mark.asyncio
async def test_startup_fails_on_first_step(dispatcher, sm, safety, planner):
    from workflows.startup import run_startup
    dispatcher.dispatch.return_value = fail("connect_drone")
    result = await run_startup(dispatcher, sm, safety, planner)
    assert result is False
    assert dispatcher.dispatch.call_count == 1  # stops immediately


@pytest.mark.asyncio
async def test_startup_with_wait_instruction(dispatcher, sm, safety, planner):
    from workflows.startup import run_startup
    responses = [
        ok("connect_drone",    state="connected", wait=WaitInstruction(0.01, "test wait")),
        ok("connect_drone",    state="connected"), # Second call after wait
        ok("get_current_state", state="connected"),
        ok("get_telemetry",    state="connected"),
        ok("get_battery",      state="connected"),
        ok("set_mode",         state="connected"),
    ]
    dispatcher.dispatch.side_effect = responses
    result = await run_startup(dispatcher, sm, safety, planner)
    assert result is True


# ── Takeoff ───────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_takeoff_success(dispatcher, sm, safety, planner):
    from workflows.takeoff import run_takeoff
    dispatcher.dispatch.return_value = ok("takeoff", state="takeoff")
    result = await run_takeoff(dispatcher, sm, safety, planner, altitude=10.0)
    assert result is True
    assert dispatcher.dispatch.call_count == 4  # set_mode, arm, takeoff, wait_altitude


@pytest.mark.asyncio
async def test_takeoff_arm_failure(dispatcher, sm, safety, planner):
    from workflows.takeoff import run_takeoff
    dispatcher.dispatch.side_effect = [
        ok("set_mode",  state="connected"),
        fail("arm_drone", error="ILLEGAL_COMMAND"),
    ]
    result = await run_takeoff(dispatcher, sm, safety, planner, altitude=10.0)
    assert result is False


# ── Navigation ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_navigation_success(dispatcher, sm, safety, planner):
    from workflows.navigation import run_navigation
    dispatcher.dispatch.return_value = ok("goto_position", state="enroute")
    result = await run_navigation(
        dispatcher, sm, safety, planner,
        lat=23.81, lon=90.41, alt=10.0
    )
    assert result is True


@pytest.mark.asyncio
async def test_navigation_with_yaw(dispatcher, sm, safety, planner):
    from workflows.navigation import run_navigation
    dispatcher.dispatch.return_value = ok("set_yaw", state="hover")
    result = await run_navigation(
        dispatcher, sm, safety, planner,
        lat=23.81, lon=90.41, alt=10.0, yaw_deg=90.0
    )
    assert result is True


# ── Return home ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_return_home_success(dispatcher, sm, safety, planner):
    from workflows.return_home import run_return_home
    safety.update_battery(80)
    dispatcher.dispatch.return_value = ok("return_to_launch", state="rtl",
                                          next_action="wait_arrival")
    dispatcher.dispatch.side_effect = [
        ok("get_battery",       state="hover",   data={"level_percent": 80}),
        ok("return_to_launch",  state="rtl"),
        ok("wait_arrival",      state="rtl"),
        ok("land",              state="landing"),
    ]
    result = await run_return_home(dispatcher, sm, safety, planner)
    assert result is True


@pytest.mark.asyncio
async def test_return_home_battery_critical_skips_to_land(dispatcher, sm, safety, planner):
    from workflows.return_home import run_return_home
    safety.update_battery(10)  # Set critical battery
    # Only need get_battery to fail/failsafe
    dispatcher.dispatch.side_effect = [
        ok("get_battery", state="hover", data={"level_percent": 10}),
    ]
    result = await run_return_home(dispatcher, sm, safety, planner)
    assert result is False  # Workflow aborted by planner failsafe
    assert dispatcher.dispatch.call_count >= 1


# ── Emergency ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_emergency_runs_to_completion(dispatcher, sm, safety, planner):
    from workflows.emergency import run_emergency
    dispatcher.dispatch.return_value = ok("land", state="landing")
    result = await run_emergency(dispatcher, sm, safety, planner, reason="test")
    assert result is True


@pytest.mark.asyncio
async def test_emergency_handles_dispatch_failure(dispatcher, sm, safety, planner):
    from workflows.emergency import run_emergency
    dispatcher.dispatch.side_effect = Exception("link lost")
    result = await run_emergency(dispatcher, sm, safety, planner, reason="link lost")
    assert result is True  # emergency always completes — never raises


# ── Intent registry ───────────────────────────────────────────────────────────

def test_intent_registry_covers_all_verbs():
    from workflows.registry import WORKFLOW_INTENTS, is_intent
    for verb in ("takeoff", "goto_position", "land", "return_to_launch", "hold_position"):
        assert is_intent(verb), f"missing intent: {verb}"
    assert not is_intent("emergency_stop")  # handled directly in app.py, not via registry
    assert not is_intent("get_status")
    assert not is_intent("nonexistent")


def test_resolve_kwargs_drops_unknown_and_none():
    from workflows.registry import resolve_kwargs
    # goto_position: speed_ms maps, yaw_deg maps, unknown key dropped, None dropped
    kwargs = resolve_kwargs("goto_position", {
        "lat":      23.8, "lon": 90.4, "alt": 10.0,
        "speed_ms": 8.0,
        "yaw_deg":  None,
        "extra":    "ignore me",
    })
    assert kwargs == {"lat": 23.8, "lon": 90.4, "alt": 10.0, "speed_ms": 8.0}


def test_resolve_kwargs_hold_position_remaps():
    from workflows.registry import resolve_kwargs
    # LLM sends `seconds` → workflow expects `hold_seconds`
    kwargs = resolve_kwargs("hold_position", {"seconds": 5.0, "yaw_deg": 90.0})
    assert kwargs == {"hold_seconds": 5.0, "yaw_deg": 90.0}
