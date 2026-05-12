"""
tests/test_thinking_oracle.py — Unit tests for ThinkingOracle.

Covers:
  - JSON parsing from content and thinking block
  - Rule fallback thresholds (mirror safety_policy.py)
  - ThinkingDecision field validation
  - Oracle gate (_should_invoke)
  - Stats tracking

Run:
    pytest tests/test_thinking_oracle.py -v
"""

import pytest
from unittest.mock import patch, MagicMock

from planner import (
    ThinkingOracle,
    ThinkingDecision,
    VALID_DECISIONS,
    HIGH_VALUE_TOOLS,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def oracle():
    return ThinkingOracle(model="droneoracle")


def make_ctx(**overrides) -> dict:
    base = {
        "tool":              "goto_position",
        "ok":                True,
        "error":             None,
        "state":             "enroute",
        "battery_pct":       80.0,
        "altitude_m":        15.0,
        "telemetry_age_sec": 1.0,
        "retry_count":       0,
        "airborne":          True,
    }
    base.update(overrides)
    return base


# ── JSON parsing ──────────────────────────────────────────────────────────────

def test_parse_json_valid(oracle):
    text = '{"decision": "CONTINUE", "next_tool": null, "wait_sec": null, "reason": "nominal", "confidence": 0.95}'
    result = oracle._parse_json(text)
    assert result is not None
    assert result.decision == "CONTINUE"
    assert result.confidence == 0.95


def test_parse_json_strips_markdown_fence(oracle):
    text = '```json\n{"decision": "WAIT", "next_tool": null, "wait_sec": 2.0, "reason": "stabilize", "confidence": 0.8}\n```'
    result = oracle._parse_json(text)
    assert result is not None
    assert result.decision == "WAIT"
    assert result.wait_sec == 2.0


def test_parse_json_invalid_decision_returns_none(oracle):
    text = '{"decision": "HOVER", "reason": "test", "confidence": 1.0}'
    result = oracle._parse_json(text)
    assert result is None


def test_parse_json_empty_returns_none(oracle):
    assert oracle._parse_json("") is None
    assert oracle._parse_json("   ") is None


def test_extract_from_thinking_finds_last(oracle):
    thinking = (
        'Analyzing... {"decision": "RETRY", "next_tool": null, "wait_sec": null, "reason": "first", "confidence": 0.5} '
        'After more analysis... {"decision": "CONTINUE", "next_tool": "wait_arrival", "wait_sec": null, "reason": "final", "confidence": 0.9}'
    )
    result = oracle._extract_from_thinking(thinking)
    assert result is not None
    assert result.decision == "CONTINUE"   # last one wins
    assert result.reason == "final"


def test_extract_from_thinking_no_json_returns_none(oracle):
    assert oracle._extract_from_thinking("no json here at all") is None


def test_extract_from_thinking_malformed_json_returns_none(oracle):
    assert oracle._extract_from_thinking('{"decision": "CONTINUE", broken}') is None


# ── Rule fallback ─────────────────────────────────────────────────────────────

def test_fallback_telemetry_emergency(oracle):
    ctx = make_ctx(telemetry_age_sec=11.0)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "FAILSAFE"
    assert td.source == "fallback"


def test_fallback_battery_critical(oracle):
    ctx = make_ctx(battery_pct=10.0)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "FAILSAFE"


def test_fallback_battery_critical_via_error(oracle):
    ctx = make_ctx(battery_pct=50.0, error="BATTERY_CRITICAL")
    td = oracle._rule_fallback(ctx)
    assert td.decision == "FAILSAFE"


def test_fallback_max_retries(oracle):
    ctx = make_ctx(ok=False, retry_count=3)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "ABORT"


def test_fallback_battery_low_airborne(oracle):
    ctx = make_ctx(battery_pct=20.0, airborne=True)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "REPLAN"


def test_fallback_battery_low_grounded(oracle):
    # Low battery but not airborne — should not REPLAN
    ctx = make_ctx(battery_pct=20.0, airborne=False, ok=False, retry_count=1)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "RETRY"


def test_fallback_transient_failure(oracle):
    ctx = make_ctx(ok=False, retry_count=1)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "RETRY"


def test_fallback_nominal(oracle):
    ctx = make_ctx(ok=True)
    td = oracle._rule_fallback(ctx)
    assert td.decision == "CONTINUE"


# ── ThinkingDecision validation ───────────────────────────────────────────────

def test_from_dict_all_valid_decisions(oracle):
    for d in VALID_DECISIONS:
        raw = {"decision": d, "reason": "test", "confidence": 1.0}
        result = ThinkingDecision._from_dict(raw)
        assert result is not None
        assert result.decision == d


def test_from_dict_lowercase_decision_normalised(oracle):
    raw = {"decision": "continue", "reason": "ok", "confidence": 0.9}
    result = ThinkingDecision._from_dict(raw)
    assert result.decision == "CONTINUE"


def test_from_dict_missing_reason_uses_empty(oracle):
    raw = {"decision": "WAIT", "confidence": 0.8}
    result = ThinkingDecision._from_dict(raw)
    assert result is not None
    assert result.reason == ""


def test_from_dict_wait_sec_parsed(oracle):
    raw = {"decision": "WAIT", "wait_sec": 3.5, "reason": "spin", "confidence": 1.0}
    result = ThinkingDecision._from_dict(raw)
    assert result.wait_sec == 3.5


def test_from_dict_none_wait_sec(oracle):
    raw = {"decision": "CONTINUE", "wait_sec": None, "reason": "ok", "confidence": 1.0}
    result = ThinkingDecision._from_dict(raw)
    assert result.wait_sec is None


# ── Oracle gate ───────────────────────────────────────────────────────────────

def test_should_invoke_high_value_tool(oracle):
    assert oracle.should_invoke("goto_position", ok=True, airborne=False) is True
    assert oracle.should_invoke("arm_drone",     ok=True, airborne=False) is True
    assert oracle.should_invoke("takeoff",       ok=True, airborne=False) is True


def test_should_invoke_on_failure(oracle):
    assert oracle.should_invoke("get_telemetry", ok=False, airborne=False) is True


def test_should_invoke_airborne(oracle):
    assert oracle.should_invoke("get_telemetry", ok=True, airborne=True) is True


def test_should_not_invoke_read_only_grounded(oracle):
    assert oracle.should_invoke("get_telemetry", ok=True,  airborne=False) is False
    assert oracle.should_invoke("get_battery",   ok=True,  airborne=False) is False
    assert oracle.should_invoke("get_position_str", ok=True, airborne=False) is False


# ── Stats ─────────────────────────────────────────────────────────────────────

def test_stats_initial(oracle):
    s = oracle.stats()
    assert s["calls"] == 0
    assert s["failures"] == 0
    assert s["fallback_rate"] == 0.0


def test_stats_increments_on_ollama_failure(oracle):
    with patch("ollama.chat", side_effect=Exception("connection refused")):
        oracle.deliberate(make_ctx())
    s = oracle.stats()
    assert s["calls"] == 1
    assert s["failures"] == 1
    assert s["fallback_rate"] == 1.0


def test_stats_no_failure_on_successful_parse(oracle):
    mock_chunk = MagicMock()
    mock_chunk.message.thinking = ""
    mock_chunk.message.content  = (
        '{"decision": "CONTINUE", "next_tool": null, '
        '"wait_sec": null, "reason": "ok", "confidence": 0.99}'
    )

    with patch("ollama.chat", return_value=iter([mock_chunk])):
        td = oracle.deliberate(make_ctx())

    assert td.decision == "CONTINUE"
    assert td.source   == "oracle"
    s = oracle.stats()
    assert s["failures"] == 0


# ── Prompt construction ───────────────────────────────────────────────────────

def test_prompt_contains_all_fields(oracle):
    ctx = make_ctx(
        tool="arm_drone", ok=False, error="timeout",
        battery_pct=45.0, altitude_m=10.5,
        telemetry_age_sec=2.3, retry_count=1, airborne=True,
    )
    prompt = oracle._build_prompt(ctx)
    assert "tool=arm_drone" in prompt
    assert "ok=False" in prompt
    assert "error=timeout" in prompt
    assert "battery=45.0%" in prompt
    assert "altitude=10.5m" in prompt
    assert "tel_age=2.3s" in prompt
    assert "retries=1" in prompt
    assert "airborne=True" in prompt


def test_prompt_no_error_shows_none(oracle):
    ctx = make_ctx(error=None)
    prompt = oracle._build_prompt(ctx)
    assert "error=none" in prompt
