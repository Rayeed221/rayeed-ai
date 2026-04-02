import pytest
from adapters.sim_adapter import SimAdapter


@pytest.fixture
def sim():
    return SimAdapter()


# ── Connection ────────────────────────────────────────────────────────────────

def test_connect(sim):
    result = sim.execute("connect_drone", {"connection_string": "udp:127.0.0.1:14550"})
    assert result["status"] == "connected"
    assert sim.is_connected() is True


def test_disconnect(sim):
    sim.execute("connect_drone", {})
    sim.disconnect()
    assert sim.is_connected() is False


# ── Telemetry ─────────────────────────────────────────────────────────────────

def test_get_telemetry_shape(sim):
    result = sim.execute("get_telemetry", {})
    assert "altitude" in result
    assert "airspeed" in result
    assert "groundspeed" in result
    assert "heading" in result


def test_get_current_state(sim):
    result = sim.execute("get_current_state", {})
    assert "mode" in result
    assert "armed" in result
    assert "system_status" in result


def test_get_position_str(sim):
    result = sim.execute("get_position_str", {})
    assert "position" in result
    assert "Lat:" in result["position"]


def test_get_battery_shape(sim):
    result = sim.execute("get_battery", {})
    assert "voltage" in result
    assert "level_percent" in result
    assert result["level_percent"] > 0


def test_battery_decrements(sim):
    b1 = sim.execute("get_battery", {})["level_percent"]
    b2 = sim.execute("get_battery", {})["level_percent"]
    assert b2 < b1


# ── Arming ────────────────────────────────────────────────────────────────────

def test_arm(sim):
    assert sim.execute("arm_drone", {})["status"] == "armed"


def test_disarm(sim):
    sim.execute("arm_drone", {})
    assert sim.execute("disarm_drone", {})["status"] == "disarmed"


# ── Flight ────────────────────────────────────────────────────────────────────

def test_takeoff_updates_altitude(sim):
    sim.execute("takeoff", {"altitude": 15.0})
    tel = sim.execute("get_telemetry", {})
    assert tel["altitude"] == 15.0


def test_land_resets_altitude(sim):
    sim.execute("takeoff", {"altitude": 20.0})
    sim.execute("land", {})
    tel = sim.execute("get_telemetry", {})
    assert tel["altitude"] == 0.0


def test_goto_position_updates_state(sim):
    result = sim.execute("goto_position", {"lat": 23.81, "lon": 90.41, "alt": 10.0})
    assert result["status"] == "moving"
    pos = sim.execute("get_position_str", {})
    assert "23.81" in pos["position"]


def test_set_speed(sim):
    result = sim.execute("set_speed", {"speed_ms": 8.0})
    assert result["speed_ms"] == 8.0


def test_set_yaw_absolute(sim):
    result = sim.execute("set_yaw", {"yaw_deg": 90.0})
    assert result["yaw_deg"] == 90.0


def test_set_yaw_relative(sim):
    sim.execute("set_yaw", {"yaw_deg": 90.0})
    result = sim.execute("set_yaw", {"yaw_deg": 45.0, "relative": True})
    assert result["yaw_deg"] == 135.0


def test_set_mode(sim):
    result = sim.execute("set_mode", {"mode": "GUIDED"})
    assert result["mode"] == "GUIDED"


# ── Wait tools ────────────────────────────────────────────────────────────────

def test_wait_altitude(sim):
    sim.execute("takeoff", {"altitude": 10.0})
    result = sim.execute("wait_altitude", {"target_alt": 10.0})
    assert result["status"] == "altitude_reached"


def test_wait_arrival(sim):
    result = sim.execute("wait_arrival", {})
    assert result["status"] == "arrived"


def test_wait_time(sim):
    result = sim.execute("wait_time", {"seconds": 2.0})
    assert result["status"] == "done"
    assert result["waited_seconds"] == 2.0


# ── Distance ─────────────────────────────────────────────────────────────────

def test_get_distance(sim):
    result = sim.execute("get_distance_to_str", {"target_lat": 23.82, "target_lon": 90.42})
    assert "distance_str" in result
    assert "bearing" in result


# ── Unknown tool ──────────────────────────────────────────────────────────────

def test_unknown_tool_returns_error(sim):
    result = sim.execute("fly_to_moon", {})
    assert "error" in result


# ── Empty args tools don't crash ──────────────────────────────────────────────

@pytest.mark.parametrize("tool", [
    "get_current_state", "get_telemetry", "get_position_str",
    "get_battery", "arm_drone", "disarm_drone",
    "land", "return_to_launch", "wait_arrival",
])
def test_no_args_tools(sim, tool):
    result = sim.execute(tool, {})
    assert isinstance(result, dict)
