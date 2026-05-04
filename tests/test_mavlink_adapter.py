"""
Tests for MAVLinkAdapter — mirrors tests/test_tools.py pattern.
All tests are synchronous: the adapter handlers are sync; asyncio.to_thread
wrapping is the dispatcher's responsibility, not tested here.
"""

import sys
import time
import pytest
from unittest.mock import MagicMock, patch

from adapters.mavlink_adapter import MAVLinkAdapter


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def mav():
    adapter = MAVLinkAdapter("udp:127.0.0.1:14550")
    conn = MagicMock()
    conn.target_system = 1
    conn.target_component = 1
    adapter._conn = conn
    return adapter, conn


def _make_heartbeat(custom_mode=4, base_mode=0x80, system_status=4):
    msg = MagicMock()
    msg.custom_mode    = custom_mode   # 4 = GUIDED
    msg.base_mode      = base_mode     # 0x80 = armed
    msg.system_status  = system_status # 4 = ACTIVE
    return msg


def _make_gps(lat_deg=23.81, lon_deg=90.41, alt_m=10.0, hdg_cdeg=9000, vx=0, vy=0):
    msg = MagicMock()
    msg.lat          = int(lat_deg * 1e7)
    msg.lon          = int(lon_deg * 1e7)
    msg.relative_alt = int(alt_m * 1000)
    msg.hdg          = hdg_cdeg
    msg.vx           = vx
    msg.vy           = vy
    return msg


def _make_vfr(airspeed=0.0, groundspeed=0.0):
    msg = MagicMock()
    msg.airspeed    = airspeed
    msg.groundspeed = groundspeed
    return msg


def _make_battery(voltage_mv=12000, current_100ma=100, level=80):
    msg = MagicMock()
    msg.voltages           = [voltage_mv, 65535]
    msg.current_battery    = current_100ma
    msg.battery_remaining  = level
    return msg


def _make_sys_status(voltage_mv=12000, current_100ma=100, level=80):
    msg = MagicMock()
    msg.voltage_battery  = voltage_mv
    msg.current_battery  = current_100ma
    msg.battery_remaining = level
    return msg


def _make_ack(result=0):  # 0 = MAV_RESULT_ACCEPTED
    msg = MagicMock()
    msg.result = result
    return msg


# ── Connection ────────────────────────────────────────────────────────────────

def _patch_mavutil(mock_conn=None, connect_side_effect=None):
    """Build sys.modules patch so `from pymavlink import mavutil` gets our mock."""
    mock_pymavlink = MagicMock()
    mock_mavutil   = mock_pymavlink.mavutil
    if connect_side_effect is not None:
        mock_mavutil.mavlink_connection.side_effect = connect_side_effect
    elif mock_conn is not None:
        mock_mavutil.mavlink_connection.return_value = mock_conn
    return mock_pymavlink, mock_mavutil


def test_connect_drone_success():
    adapter    = MAVLinkAdapter("udp:127.0.0.1:14550")
    mock_conn  = MagicMock()
    mock_pm, _ = _patch_mavutil(mock_conn=mock_conn)

    with patch.dict(sys.modules, {"pymavlink": mock_pm}):
        result = adapter._handle_connect_drone()

    assert result["status"] == "connected"
    assert "connection_string" in result
    mock_conn.wait_heartbeat.assert_called_once()


def test_connect_drone_failure():
    adapter    = MAVLinkAdapter("udp:127.0.0.1:14550")
    mock_pm, _ = _patch_mavutil(connect_side_effect=TimeoutError("no heartbeat"))

    with patch.dict(sys.modules, {"pymavlink": mock_pm}):
        result = adapter._handle_connect_drone()

    assert "error" in result


def test_unknown_tool_returns_error(mav):
    adapter, _ = mav
    result = adapter.execute("fly_to_moon", {})
    assert "error" in result


# ── State / Telemetry shape (safety_policy reads these exact keys) ─────────────

def test_get_current_state_shape(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_heartbeat()
    result = adapter.execute("get_current_state", {})
    assert "mode" in result
    assert "armed" in result
    assert "system_status" in result
    assert isinstance(result["armed"], bool)


def test_get_current_state_no_heartbeat(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None
    result = adapter.execute("get_current_state", {})
    assert "error" in result


def test_get_telemetry_shape(mav):
    adapter, conn = mav

    def _recv(type, blocking=True, timeout=5.0):
        if type == "GLOBAL_POSITION_INT":
            return _make_gps()
        if type == "VFR_HUD":
            return _make_vfr()
        return None

    conn.recv_match.side_effect = _recv
    result = adapter.execute("get_telemetry", {})
    assert "altitude"    in result
    assert "airspeed"    in result
    assert "groundspeed" in result
    assert "heading"     in result


def test_get_telemetry_no_gps(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None
    result = adapter.execute("get_telemetry", {})
    assert "error" in result


def test_get_position_str_shape(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_gps()
    result = adapter.execute("get_position_str", {})
    assert "position" in result
    assert "Lat:" in result["position"]
    assert "Lon:" in result["position"]


def test_get_position_str_no_gps(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None
    result = adapter.execute("get_position_str", {})
    assert "error" in result


# ── Battery — level_percent key is safety-critical ───────────────────────────

def test_get_battery_level_percent_key(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_battery()
    result = adapter.execute("get_battery", {})
    assert "level_percent" in result, "safety_policy reads 'level_percent' — key name is non-negotiable"
    assert "voltage" in result
    assert "current" in result


def test_get_battery_fallback_to_sys_status(mav):
    adapter, conn = mav
    call_count = [0]

    def _recv(type, blocking=True, timeout=5.0):
        call_count[0] += 1
        if type == "BATTERY_STATUS":
            return None  # not available
        if type == "SYS_STATUS":
            return _make_sys_status()
        return None

    conn.recv_match.side_effect = _recv
    result = adapter.execute("get_battery", {})
    assert "level_percent" in result
    assert result["level_percent"] == 80.0


def test_get_battery_no_message(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None
    result = adapter.execute("get_battery", {})
    assert "error" in result


def test_get_battery_unknown_level_estimated_from_voltage(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_battery(voltage_mv=11800, level=-1)
    result = adapter.execute("get_battery", {})
    assert "level_percent" in result
    assert 0.0 <= result["level_percent"] <= 100.0


# ── Distance ──────────────────────────────────────────────────────────────────

def test_get_distance_to_str_shape(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_gps()
    result = adapter.execute("get_distance_to_str", {"target_lat": 23.82, "target_lon": 90.42})
    assert "distance_str" in result
    assert "bearing" in result
    assert "meters" in result["distance_str"]


def test_get_distance_to_str_no_gps(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None
    result = adapter.execute("get_distance_to_str", {"target_lat": 23.82, "target_lon": 90.42})
    assert "error" in result


# ── Mode setting ──────────────────────────────────────────────────────────────

def test_set_mode_success(mav):
    adapter, conn = mav
    hb = _make_heartbeat(custom_mode=4)  # 4 = GUIDED

    conn.recv_match.return_value = hb
    result = adapter.execute("set_mode", {"mode": "GUIDED"})
    assert result.get("status") == "ok"
    assert result.get("mode") == "GUIDED"


def test_set_mode_unknown_mode(mav):
    adapter, _ = mav
    result = adapter.execute("set_mode", {"mode": "TURBO_BOOST"})
    assert "error" in result


def test_set_mode_timeout(mav):
    adapter, conn = mav
    # Always return wrong mode → never confirms
    hb = _make_heartbeat(custom_mode=0)  # 0 = STABILIZE, not GUIDED
    conn.recv_match.return_value = hb

    with patch("adapters.mavlink_adapter.time.monotonic", side_effect=[0.0, 0.0, 6.0]):
        result = adapter.execute("set_mode", {"mode": "GUIDED"})
    assert "error" in result


# ── Arming ────────────────────────────────────────────────────────────────────

def test_arm_drone_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_ack(result=0)
    result = adapter.execute("arm_drone", {})
    assert result.get("status") == "armed"


def test_arm_drone_failure(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_ack(result=4)  # MAV_RESULT_FAILED
    result = adapter.execute("arm_drone", {})
    assert "error" in result


def test_disarm_drone_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_ack(result=0)
    result = adapter.execute("disarm_drone", {})
    assert result.get("status") == "disarmed"


def test_disarm_drone_no_ack(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None
    result = adapter.execute("disarm_drone", {})
    assert "error" in result


# ── Flight commands ────────────────────────────────────────────────────────────

def test_land_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_heartbeat(custom_mode=9)  # 9 = LAND
    result = adapter.execute("land", {})
    assert result.get("status") == "landing"


def test_return_to_launch_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_heartbeat(custom_mode=6)  # 6 = RTL
    result = adapter.execute("return_to_launch", {})
    assert result.get("status") == "returning_to_launch"


def test_set_yaw_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_ack(result=0)
    result = adapter.execute("set_yaw", {"yaw_deg": 90.0})
    assert result.get("status") == "ok"
    assert result.get("yaw_deg") == 90.0


def test_set_yaw_failure(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_ack(result=4)
    result = adapter.execute("set_yaw", {"yaw_deg": 90.0})
    assert "error" in result


def test_set_speed_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_ack(result=0)
    result = adapter.execute("set_speed", {"speed_ms": 5.0})
    assert result.get("status") == "ok"
    assert result.get("speed_ms") == 5.0


def test_set_speed_failure(mav):
    adapter, conn = mav
    conn.recv_match.return_value = None  # no ack
    result = adapter.execute("set_speed", {"speed_ms": 5.0})
    assert "error" in result


def test_goto_position_success(mav):
    adapter, conn = mav
    # set_mode confirmation + mav.set_position_target_global_int_send (no return value needed)
    conn.recv_match.return_value = _make_heartbeat(custom_mode=4)  # GUIDED confirmed

    mock_pm = MagicMock()
    mock_pm.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT = 6
    # set_mode confirmation — HEARTBEAT already handled by conn.recv_match above

    with patch.dict(sys.modules, {"pymavlink": mock_pm}):
        result = adapter.execute("goto_position", {"lat": 23.82, "lon": 90.42, "alt": 10.0})

    assert result.get("status") == "moving"
    assert result["target"]["lat"] == 23.82
    assert result["target"]["lon"] == 90.42
    assert result["target"]["alt"] == 10.0


# ── Wait tools ────────────────────────────────────────────────────────────────

def test_wait_time_zero(mav):
    adapter, _ = mav
    result = adapter.execute("wait_time", {"seconds": 0.0})
    assert result.get("status") == "done"
    assert result.get("waited_seconds") == 0.0


def test_wait_altitude_success(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_gps(alt_m=10.0)
    result = adapter.execute("wait_altitude", {"target_alt": 10.0, "tolerance": 0.5})
    assert result.get("status") == "altitude_reached"
    assert "altitude" in result


def test_wait_altitude_timeout(mav):
    adapter, conn = mav
    conn.recv_match.return_value = _make_gps(alt_m=0.0)  # never reaches target

    with patch("adapters.mavlink_adapter.time.monotonic", side_effect=[0.0, 0.0, 61.0]):
        with patch("adapters.mavlink_adapter.time.sleep"):
            result = adapter.execute("wait_altitude", {"target_alt": 50.0})
    assert "error" in result


def test_wait_arrival_success(mav):
    adapter, conn = mav
    still = _make_vfr(groundspeed=0.1)  # < 0.5 m/s → "stable"
    conn.recv_match.return_value = still

    with patch("adapters.mavlink_adapter.time.sleep"):
        result = adapter.execute("wait_arrival", {})
    assert result.get("status") == "arrived"


def test_wait_arrival_timeout(mav):
    adapter, conn = mav
    moving = _make_vfr(groundspeed=5.0)  # never stable
    conn.recv_match.return_value = moving

    with patch("adapters.mavlink_adapter.time.monotonic", side_effect=[0.0, 0.0, 121.0]):
        with patch("adapters.mavlink_adapter.time.sleep"):
            result = adapter.execute("wait_arrival", {})
    assert "error" in result


# ── Takeoff ───────────────────────────────────────────────────────────────────

def test_takeoff_success(mav):
    adapter, conn = mav

    call_n = [0]

    def _recv(type, blocking=True, timeout=5.0):
        call_n[0] += 1
        if type == "HEARTBEAT":
            return _make_heartbeat(custom_mode=4)  # GUIDED confirmed
        if type == "COMMAND_ACK":
            return _make_ack(result=0)
        return None

    conn.recv_match.side_effect = _recv
    result = adapter.execute("takeoff", {"altitude": 10.0})
    assert result.get("status") == "taking_off"
    assert result.get("target_altitude") == 10.0


def test_takeoff_mode_failure(mav):
    adapter, conn = mav
    # HEARTBEAT always returns wrong mode → set_mode fails
    conn.recv_match.return_value = _make_heartbeat(custom_mode=0)

    with patch("adapters.mavlink_adapter.time.monotonic", side_effect=[0.0, 0.0, 6.0]):
        result = adapter.execute("takeoff", {"altitude": 10.0})
    assert "error" in result
