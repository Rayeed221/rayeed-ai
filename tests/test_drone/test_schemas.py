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


# ── Compact wire format (latency) ─────────────────────────────────────────────

def test_to_llm_drops_null_and_default_fields():
    resp = ToolResponse.success(
        tool="get_battery", state="hover",
        data={"voltage": 11.8, "level_percent": 78.0},
    )
    out = resp.to_llm()
    assert out == {
        "ok": True,
        "tool": "get_battery",
        "state": "hover",
        "data": {"voltage": 11.8, "level_percent": 78.0},
    }
    # The model never reads these, and every field is re-tokenised per turn.
    for dropped in ("timestamp", "error", "next_action", "wait", "confidence"):
        assert dropped not in out


def test_to_llm_keeps_everything_the_model_reasons_over():
    resp = ToolResponse.success(
        tool="takeoff", state="takeoff",
        data={"target_altitude": 10.0},
        next_action="wait_altitude",
        wait=WaitInstruction(seconds=2.0, reason="stabilize"),
        confidence=0.8,
    )
    out = resp.to_llm()
    assert out["data"] == {"target_altitude": 10.0}
    assert out["next_action"] == "wait_altitude"
    assert out["wait"] == {"seconds": 2.0, "reason": "stabilize"}
    assert out["confidence"] == 0.8


def test_to_llm_keeps_error_on_failure():
    resp = ToolResponse.failure(
        tool="goto_position", state="enroute",
        error="AVOIDANCE_ACTIVE: obstacle ahead", next_action="retry",
    )
    out = resp.to_llm()
    assert out["ok"] is False
    assert out["error"] == "AVOIDANCE_ACTIVE: obstacle ahead"
    assert out["next_action"] == "retry"
    assert out["confidence"] == 0.0     # not the default, so it is kept


def test_to_llm_is_smaller_than_to_dict():
    import json
    resp = ToolResponse.success(
        tool="get_telemetry", state="hover",
        data={"altitude": 10.0, "airspeed": 0.0, "groundspeed": 0.0, "heading": 271.0},
    )
    assert len(json.dumps(resp.to_llm())) < len(json.dumps(resp.to_dict()))


def test_sentence_is_one_compact_line():
    ok_resp = ToolResponse.success(tool="takeoff", state="hover",
                                   next_action="wait_altitude")
    assert ok_resp.sentence() == "OK takeoff | hover | next=wait_altitude"

    err_resp = ToolResponse.failure(tool="arm_drone", state="connected",
                                    error="rejected (result=4)")
    line = err_resp.sentence()
    assert line.startswith("ERR arm_drone | connected")
    assert "\n" not in line
