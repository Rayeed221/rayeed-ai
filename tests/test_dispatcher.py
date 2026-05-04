"""
Integration tests for ToolDispatcher — tests the full 7-step pipeline
using real SafetyPolicy + StateMachine with a mocked adapter.
"""

import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from schemas import ToolResponse
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy
from tool_dispatcher import ToolDispatcher, TOOL_TIMEOUT_SEC


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sm():
    return StateMachine()


@pytest.fixture
def safety(sm):
    return SafetyPolicy(sm)


@pytest.fixture
def mock_adapter():
    a = MagicMock()
    a.execute = MagicMock(return_value={"status": "ok"})
    return a


@pytest.fixture
def dispatcher(sm, safety, mock_adapter):
    return ToolDispatcher(sm, safety, mock_adapter)


# ── Safety gate: battery critical blocks before adapter ───────────────────────

@pytest.mark.asyncio
async def test_battery_critical_blocks_takeoff(sm, safety, mock_adapter):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    safety.update_battery(10.0)  # below BATTERY_CRITICAL_PCT (15%)

    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("takeoff", {"altitude": 10.0})

    assert resp.ok is False
    assert "BATTERY_CRITICAL" in resp.error
    mock_adapter.execute.assert_not_called()


# ── Safety gate: command legality blocks wrong-state commands ─────────────────

@pytest.mark.asyncio
async def test_illegal_command_in_idle_blocked(sm, safety, mock_adapter):
    # sm starts in IDLE — arm_drone requires CONNECTED state
    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("arm_drone", {})

    assert resp.ok is False
    assert "ILLEGAL_COMMAND" in resp.error
    mock_adapter.execute.assert_not_called()


@pytest.mark.asyncio
async def test_read_tool_allowed_in_any_state(sm, safety, mock_adapter):
    # get_telemetry has no state restriction — should reach the adapter
    mock_adapter.execute.return_value = {
        "altitude": 0.0, "airspeed": 0.0, "groundspeed": 0.0, "heading": 0.0
    }
    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("get_telemetry", {})

    assert resp.ok is True
    mock_adapter.execute.assert_called_once()


# ── Adapter timeout increments retry counter ─────────────────────────────────

@pytest.mark.asyncio
async def test_adapter_timeout_increments_retry(sm, safety, mock_adapter):
    import time
    mock_adapter.execute.side_effect = lambda *a, **kw: time.sleep(15)

    d = ToolDispatcher(sm, safety, mock_adapter)
    with patch("tool_dispatcher.TOOL_TIMEOUT_SEC", 0.05):
        resp = await d.dispatch("get_current_state", {})

    assert resp.ok is False
    assert "timed out" in resp.error
    assert safety._retry_counts.get("get_current_state", 0) == 1


# ── Retry counter resets on success ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_retry_counter_resets_on_success(sm, safety, mock_adapter):
    safety.increment_retry("get_current_state")
    assert safety._retry_counts.get("get_current_state") == 1

    mock_adapter.execute.return_value = {
        "mode": "GUIDED", "armed": False, "system_status": "ACTIVE"
    }
    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("get_current_state", {})

    assert resp.ok is True
    assert safety._retry_counts.get("get_current_state", 0) == 0


# ── Geofence blocks goto_position outside radius ─────────────────────────────

@pytest.mark.asyncio
async def test_geofence_breach_blocks_goto(sm, safety, mock_adapter):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    sm.transition(MissionState.HOVER)
    safety.set_home(23.81, 90.41)

    d = ToolDispatcher(sm, safety, mock_adapter)
    # ~1200m away from home — exceeds 500m default
    resp = await d.dispatch("goto_position", {"lat": 23.82, "lon": 90.41, "alt": 10.0})

    assert resp.ok is False
    assert "GEOFENCE_BREACH" in resp.error
    mock_adapter.execute.assert_not_called()


@pytest.mark.asyncio
async def test_goto_within_geofence_passes(sm, safety, mock_adapter):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    sm.transition(MissionState.HOVER)
    safety.set_home(23.81, 90.41)

    mock_adapter.execute.return_value = {
        "status": "moving", "target": {"lat": 23.8103, "lon": 90.4102, "alt": 10.0}
    }
    d = ToolDispatcher(sm, safety, mock_adapter)
    # ~50m away — within radius
    resp = await d.dispatch(
        "goto_position", {"lat": 23.8105, "lon": 90.4105, "alt": 10.0}
    )

    assert resp.ok is True
    mock_adapter.execute.assert_called_once()


# ── Vision tools bypass safety checks ────────────────────────────────────────

@pytest.mark.asyncio
async def test_vision_tool_bypasses_safety(sm, safety, mock_adapter):
    mock_vision = MagicMock()
    mock_vision.execute.return_value = {"depth_grid": []}

    d = ToolDispatcher(sm, safety, mock_adapter, vision_tool=mock_vision)

    with patch.object(safety, "pre_execute_check") as mock_check:
        resp = await d.dispatch("vision_depth_snapshot", {})

    mock_check.assert_not_called()
    mock_adapter.execute.assert_not_called()
    mock_vision.execute.assert_called_once()


# ── Adapter error response increments retry ───────────────────────────────────

@pytest.mark.asyncio
async def test_adapter_error_dict_increments_retry(sm, safety, mock_adapter):
    mock_adapter.execute.return_value = {"error": "hardware fault"}

    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("get_current_state", {})

    assert resp.ok is False
    assert safety._retry_counts.get("get_current_state", 0) == 1


# ── State machine transitions on success ─────────────────────────────────────

@pytest.mark.asyncio
async def test_connect_drone_transitions_to_connected(sm, safety, mock_adapter):
    mock_adapter.execute.return_value = {
        "status": "connected", "connection_string": "udp:127.0.0.1:14550"
    }
    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("connect_drone", {})

    assert resp.ok is True
    assert sm.state == MissionState.CONNECTED


# ── set_home captured from get_position_str ───────────────────────────────────

@pytest.mark.asyncio
async def test_get_position_str_sets_home(sm, safety, mock_adapter):
    mock_adapter.execute.return_value = {
        "position": "Lat: 23.810000, Lon: 90.412500, Alt: 0.0m"
    }
    assert safety._home_lat is None

    d = ToolDispatcher(sm, safety, mock_adapter)
    resp = await d.dispatch("get_position_str", {})

    assert resp.ok is True
    assert safety._home_lat == pytest.approx(23.81, abs=1e-4)
    assert safety._home_lon == pytest.approx(90.4125, abs=1e-4)


@pytest.mark.asyncio
async def test_home_set_only_once(sm, safety, mock_adapter):
    mock_adapter.execute.return_value = {
        "position": "Lat: 23.810000, Lon: 90.412500, Alt: 0.0m"
    }
    d = ToolDispatcher(sm, safety, mock_adapter)
    await d.dispatch("get_position_str", {})
    first_lat = safety._home_lat

    mock_adapter.execute.return_value = {
        "position": "Lat: 24.000000, Lon: 91.000000, Alt: 5.0m"
    }
    await d.dispatch("get_position_str", {})

    # home must not be overwritten after first capture
    assert safety._home_lat == first_lat
