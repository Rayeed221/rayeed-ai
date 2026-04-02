import time
import pytest
from schemas import ToolResponse, WaitInstruction, MissionEvent, ErrorSchema


def test_success_shape():
    resp = ToolResponse.success(
        tool="takeoff", state="takeoff",
        data={"altitude": 10.0},
        next_action="wait_altitude",
        wait=WaitInstruction(seconds=2.0, reason="stabilize"),
        confidence=0.95,
    )
    assert resp.ok is True
    assert resp.tool == "takeoff"
    assert resp.state == "takeoff"
    assert resp.data["altitude"] == 10.0
    assert resp.next_action == "wait_altitude"
    assert resp.wait.seconds == 2.0
    assert resp.wait.reason == "stabilize"
    assert resp.confidence == 0.95
    assert resp.error is None


def test_failure_shape():
    resp = ToolResponse.failure(
        tool="arm_drone", state="idle",
        error="ILLEGAL_COMMAND",
        next_action="get_current_state",
    )
    assert resp.ok is False
    assert resp.error == "ILLEGAL_COMMAND"
    assert resp.confidence == 0.0
    assert resp.data == {}


def test_wait_is_none_by_default():
    resp = ToolResponse.success(tool="get_battery", state="connected", data={})
    assert resp.wait is None


def test_to_dict_is_serializable():
    resp = ToolResponse.success(
        tool="land", state="landing",
        wait=WaitInstruction(seconds=1.0, reason="ground contact"),
    )
    d = resp.to_dict()
    assert isinstance(d, dict)
    assert d["wait"]["seconds"] == 1.0
    assert d["wait"]["reason"] == "ground contact"
    assert d["ok"] is True


def test_failure_to_dict():
    resp = ToolResponse.failure(tool="takeoff", state="idle", error="BATTERY_CRITICAL")
    d = resp.to_dict()
    assert d["ok"] is False
    assert d["error"] == "BATTERY_CRITICAL"
    assert d["wait"] is None


def test_timestamp_auto_set():
    before = time.time()
    resp = ToolResponse.success(tool="test", state="idle")
    after = time.time()
    assert before <= resp.timestamp <= after


def test_mission_event_shape():
    ev = MissionEvent(event_type="tool_call", tool="takeoff", state="takeoff")
    d = ev.to_dict()
    assert d["event_type"] == "tool_call"
    assert d["tool"] == "takeoff"
    assert isinstance(d["timestamp"], float)


def test_error_schema():
    err = ErrorSchema(
        code="BATTERY_CRITICAL",
        message="Battery at 10%",
        retryable=False,
        context={"pct": 10},
    )
    assert err.retryable is False
    d = err.to_dict()
    assert d["code"] == "BATTERY_CRITICAL"
    assert d["context"]["pct"] == 10


def test_wait_instruction_dict():
    w = WaitInstruction(seconds=3.5, reason="RTL init")
    d = w.to_dict()
    assert d == {"seconds": 3.5, "reason": "RTL init"}
