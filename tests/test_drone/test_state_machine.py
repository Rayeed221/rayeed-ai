import pytest
from state_machine import StateMachine, MissionState, IllegalTransitionError


@pytest.fixture
def sm():
    return StateMachine()


def test_initial_state(sm):
    assert sm.state == MissionState.IDLE


def test_legal_transition(sm):
    sm.transition(MissionState.CONNECTED)
    assert sm.state == MissionState.CONNECTED


def test_illegal_transition_raises(sm):
    with pytest.raises(IllegalTransitionError):
        sm.transition(MissionState.TAKEOFF)  # IDLE → TAKEOFF is illegal


def test_illegal_skip_states(sm):
    with pytest.raises(IllegalTransitionError):
        sm.transition(MissionState.ARMED)    # IDLE → ARMED is illegal


def test_full_legal_flight_sequence(sm):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    sm.transition(MissionState.HOVER)
    sm.transition(MissionState.ENROUTE)
    sm.transition(MissionState.HOVER)
    sm.transition(MissionState.RTL)
    sm.transition(MissionState.LANDING)
    sm.transition(MissionState.IDLE)
    assert sm.state == MissionState.IDLE


def test_force_failsafe_always_works(sm):
    sm.force_failsafe()
    assert sm.state == MissionState.FAILSAFE


def test_force_failsafe_from_mid_flight(sm):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    sm.force_failsafe()
    assert sm.state == MissionState.FAILSAFE


def test_recover_from_failsafe_to_idle(sm):
    sm.force_failsafe()
    sm.transition(MissionState.IDLE)
    assert sm.state == MissionState.IDLE


def test_illegal_from_failsafe(sm):
    sm.force_failsafe()
    with pytest.raises(IllegalTransitionError):
        sm.transition(MissionState.CONNECTED)  # must go through IDLE first


def test_is_airborne_false_on_ground(sm):
    assert sm.is_airborne() is False


def test_is_airborne_true_in_flight(sm):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    assert sm.is_airborne() is True


def test_is_airborne_false_after_landing(sm):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    sm.transition(MissionState.TAKEOFF)
    sm.transition(MissionState.HOVER)
    sm.transition(MissionState.LANDING)
    assert sm.is_airborne() is False


def test_history_records_transitions(sm):
    sm.transition(MissionState.CONNECTED)
    sm.transition(MissionState.ARMED)
    h = sm.history()
    assert len(h) == 2
    assert h[0] == (MissionState.IDLE, MissionState.CONNECTED)
    assert h[1] == (MissionState.CONNECTED, MissionState.ARMED)


def test_to_dict(sm):
    sm.transition(MissionState.CONNECTED)
    d = sm.to_dict()
    assert d["state"] == "connected"
    assert len(d["history"]) == 1


def test_failsafe_recorded_in_history(sm):
    sm.force_failsafe()
    h = sm.history()
    assert h[-1] == (MissionState.IDLE, MissionState.FAILSAFE)
