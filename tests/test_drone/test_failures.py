import time
import pytest
from unittest.mock import AsyncMock

from schemas import ToolResponse, WaitInstruction
from state_machine import StateMachine, MissionState
from safety_policy import SafetyPolicy
from planner import Planner, PlanDecision


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sm():
    return StateMachine()

@pytest.fixture
def safety(sm):
    return SafetyPolicy(sm)

@pytest.fixture
def dispatcher():
    return AsyncMock()

@pytest.fixture
def planner(sm, safety, dispatcher):
    return Planner(sm, safety, dispatcher)


# ── Planner decisions — reflex tier ───────────────────────────────────────────
#
# These assert the decision contract on the synchronous reflex tier, which is
# what resolves every one of these cases with no model in the loop.  The async
# decide() wrapper is covered below.

def test_reflex_failsafe_when_in_failsafe_state(sm, safety, dispatcher, planner):
    sm.force_failsafe()
    resp = ToolResponse.failure(tool="takeoff", state="failsafe", error="anything")
    assert planner.reflex(resp).decision == PlanDecision.FAILSAFE


def test_reflex_failsafe_on_battery_critical_error(planner):
    resp = ToolResponse.failure(tool="arm_drone", state="connected", error="BATTERY_CRITICAL")
    assert planner.reflex(resp).decision == PlanDecision.FAILSAFE


def test_reflex_failsafe_on_telemetry_emergency(planner):
    resp = ToolResponse.failure(tool="get_telemetry", state="hover", error="TELEMETRY_EMERGENCY")
    assert planner.reflex(resp).decision == PlanDecision.FAILSAFE


def test_reflex_failsafe_on_emergency_next_action(planner):
    resp = ToolResponse.failure(tool="arm_drone", state="idle", error="MAX_RETRIES", next_action="emergency")
    assert planner.reflex(resp).decision == PlanDecision.FAILSAFE


def test_reflex_retry_on_retryable(planner):
    resp = ToolResponse.failure(tool="get_telemetry", state="connected",
                                error="timeout", next_action="retry")
    assert planner.reflex(resp).decision == PlanDecision.RETRY


def test_reflex_wait_on_wait_instruction(planner):
    resp = ToolResponse.success(
        tool="takeoff", state="takeoff",
        wait=WaitInstruction(seconds=2.0, reason="stabilize"),
    )
    assert planner.reflex(resp).decision == PlanDecision.WAIT


def test_reflex_continue_on_clean_success(planner):
    resp = ToolResponse.success(tool="arm_drone", state="armed", next_action="takeoff")
    assert planner.reflex(resp).decision == PlanDecision.CONTINUE


def test_reflex_abort_on_non_retryable_failure(planner):
    resp = ToolResponse.failure(tool="arm_drone", state="idle",
                                error="ILLEGAL_COMMAND", next_action=None)
    assert planner.reflex(resp).decision == PlanDecision.ABORT


def test_reflex_replan_on_battery_low(planner, safety):
    safety.update_battery(20.0)  # 20% — below BATTERY_LOW_PCT (25%)
    resp = ToolResponse.success(tool="goto_position", state="enroute", next_action="wait_arrival")
    assert planner.reflex(resp).decision == PlanDecision.REPLAN


# ── Reflex tier keeps the oracle out of the hot path ──────────────────────────

def test_reflex_is_definite_for_nominal_airborne_call(planner, sm):
    """A successful in-flight call must not need deliberation — this is the
    case that used to invoke the local LLM on every single tool call."""
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    sm.transition(MissionState.HOVER)
    resp = ToolResponse.success(tool="goto_position", state="hover")
    reflex = planner.reflex(resp)
    assert reflex.is_definite() is True
    assert reflex.decision == PlanDecision.CONTINUE


def test_reflex_escalates_repeated_critical_failure(planner, safety):
    """A *repeated* failure of a flight-critical tool is the ambiguous case
    that is still worth deliberating on."""
    safety.increment_retry("goto_position")
    resp = ToolResponse.failure(tool="goto_position", state="enroute",
                                error="link timeout", next_action="retry")
    reflex = planner.reflex(resp)
    assert reflex.is_definite() is False


@pytest.mark.asyncio
async def test_decide_uses_reflex_without_oracle(planner, monkeypatch):
    """decide() must answer nominal calls without touching the oracle."""
    def _boom(_ctx):
        raise AssertionError("oracle must not be consulted on a nominal result")

    monkeypatch.setattr(planner._oracle, "deliberate", _boom)
    resp = ToolResponse.success(tool="arm_drone", state="armed", next_action="takeoff")
    assert await planner.decide(resp) == PlanDecision.CONTINUE
    assert planner.decision_stats()["escalations"] == 0


@pytest.mark.asyncio
async def test_decide_falls_back_when_oracle_exceeds_deadline(planner, safety, monkeypatch):
    """A slow oracle must never hold up the tool result past its deadline."""
    import planner as planner_mod

    def _slow(_ctx):
        time.sleep(2.0)
        raise AssertionError("should have been abandoned at the deadline")

    monkeypatch.setattr(planner_mod, "ORACLE_DEADLINE_SEC", 0.05)
    monkeypatch.setattr(planner._oracle, "deliberate", _slow)

    safety.increment_retry("goto_position")
    resp = ToolResponse.failure(tool="goto_position", state="enroute",
                                error="link timeout", next_action="retry")

    t0 = time.monotonic()
    decision = await planner.decide(resp)
    elapsed = time.monotonic() - t0

    assert decision == PlanDecision.RETRY          # rule tier answered
    assert elapsed < 1.0                            # deadline was enforced
    assert planner.decision_stats()["oracle_timeouts"] == 1


# ── Non-blocking wait ──────────────────────────────────────────────────────────

def test_wait_is_active_immediately_after_schedule(planner):
    planner.schedule_wait(WaitInstruction(seconds=5.0, reason="test"))
    assert planner.is_waiting() is True


def test_wait_expires_after_duration(planner):
    planner.schedule_wait(WaitInstruction(seconds=0.01, reason="short"))
    time.sleep(0.05)
    assert planner.is_waiting() is False


def test_wait_remaining_decreases(planner):
    planner.schedule_wait(WaitInstruction(seconds=1.0, reason="test"))
    r1 = planner.wait_remaining()
    time.sleep(0.05)
    r2 = planner.wait_remaining()
    assert r2 < r1


def test_no_wait_remaining_without_schedule(planner):
    assert planner.wait_remaining() == 0.0


# ── Safety policy ─────────────────────────────────────────────────────────────

def test_battery_critical(sm):
    s = SafetyPolicy(sm)
    s.update_battery(10.0)
    err = s.check_battery()
    assert err.code == "BATTERY_CRITICAL"
    assert err.retryable is False


def test_battery_low(sm):
    s = SafetyPolicy(sm)
    s.update_battery(20.0)
    err = s.check_battery()
    assert err.code == "BATTERY_LOW"
    assert err.retryable is True


def test_battery_ok(sm):
    s = SafetyPolicy(sm)
    s.update_battery(80.0)
    assert s.check_battery() is None


def test_altitude_ceiling_exceeded(sm):
    s = SafetyPolicy(sm)
    err = s.check_altitude(target_alt=200.0)
    assert err.code == "ALTITUDE_CEILING"
    assert err.retryable is False


def test_altitude_ok(sm):
    s = SafetyPolicy(sm)
    assert s.check_altitude(target_alt=50.0) is None


def test_speed_exceeded(sm):
    s = SafetyPolicy(sm)
    err = s.check_speed(speed_ms=20.0)
    assert err.code == "SPEED_EXCEEDED"


def test_speed_ok(sm):
    s = SafetyPolicy(sm)
    assert s.check_speed(speed_ms=10.0) is None


def test_telemetry_stale(sm):
    s = SafetyPolicy(sm)
    s._last_tel_time = time.time() - 6.0  # 6s ago — stale threshold is 5s
    err = s.check_telemetry_freshness()
    assert err.code == "TELEMETRY_STALE"
    assert err.retryable is True


def test_telemetry_emergency(sm):
    s = SafetyPolicy(sm)
    s._last_tel_time = time.time() - 11.0  # 11s ago — emergency threshold is 10s
    err = s.check_telemetry_freshness()
    assert err.code == "TELEMETRY_EMERGENCY"
    assert err.retryable is False


def test_telemetry_fresh(sm):
    s = SafetyPolicy(sm)
    s.update_telemetry_timestamp()
    assert s.check_telemetry_freshness() is None


def test_retry_limit_reached(sm):
    s = SafetyPolicy(sm)
    for _ in range(3):
        s.increment_retry("takeoff")
    err = s.check_retry_limit("takeoff")
    assert err.code == "MAX_RETRIES"
    assert err.retryable is False


def test_retry_reset_clears_count(sm):
    s = SafetyPolicy(sm)
    s.increment_retry("arm_drone")
    s.increment_retry("arm_drone")
    s.reset_retry("arm_drone")
    assert s.check_retry_limit("arm_drone") is None


def test_retry_below_limit(sm):
    s = SafetyPolicy(sm)
    s.increment_retry("land")
    assert s.check_retry_limit("land") is None


# ── Command legality ──────────────────────────────────────────────────────────

def test_illegal_command_in_wrong_state(sm):
    s = SafetyPolicy(sm)
    # arm_drone requires CONNECTED, sm is in IDLE
    err = s.check_command_legality("arm_drone", sm.state)
    assert err.code == "ILLEGAL_COMMAND"


def test_legal_command_in_correct_state(sm):
    s = SafetyPolicy(sm)
    sm.transition(MissionState.CONNECTED)
    err = s.check_command_legality("arm_drone", sm.state)
    assert err is None


def test_unknown_tool_is_caught(sm):
    s = SafetyPolicy(sm)
    err = s.check_command_legality("fly_backwards", sm.state)
    assert err.code == "UNKNOWN_TOOL"


def test_read_tool_allowed_in_any_state(sm):
    s = SafetyPolicy(sm)
    # get_telemetry has allowed_states=None → always legal
    err = s.check_command_legality("get_telemetry", sm.state)
    assert err is None
