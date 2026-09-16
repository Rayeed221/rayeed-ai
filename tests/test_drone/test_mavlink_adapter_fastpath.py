"""
tests/test_drone/test_mavlink_adapter_fastpath.py — cached-read fast paths.

These cover the handlers rewritten for latency: reads that now hit the message
cache instead of issuing a blocking recv_match(), and set_mode's no-op when the
vehicle is already in the requested mode.  A fake connection and a fake cache
stand in for pymavlink, so the tests need no hardware and no pymavlink install.
"""

import time

import pytest

from adapters.mavlink_adapter import MAVLinkAdapter


# ── Fakes ─────────────────────────────────────────────────────────────────────

class FakeMsg:
    def __init__(self, msg_type="HEARTBEAT", **fields):
        self._type = msg_type
        for k, v in fields.items():
            setattr(self, k, v)

    def get_type(self):
        return self._type

    def get_srcSystem(self):
        return 1


class FakeCache:
    """Serves messages from a dict; records every wait so the tests can assert
    that the fast paths did not fall back to waiting."""

    def __init__(self, messages=None):
        self.messages = dict(messages or {})
        self.waits    = []
        self.acks     = {}

    def get(self, msg_type, max_age=None):
        return self.messages.get(msg_type)

    def get_with_ts(self, msg_type, max_age=None):
        msg = self.messages.get(msg_type)
        return (msg, time.monotonic()) if msg is not None else (None, None)

    def age(self, msg_type):
        return 0.0 if msg_type in self.messages else None

    def wait(self, msg_type, timeout=5.0, max_age=None, match=None):
        self.waits.append(msg_type)
        msg = self.messages.get(msg_type)
        if msg is not None and (match is None or match(msg)):
            return msg
        return None

    def wait_ack(self, command, since, timeout=10.0):
        return self.acks.get(command)

    def stats(self):
        return {"running": True, "errors": 0, "ages_sec": {}}


class FakeMav:
    def __init__(self):
        self.sent = []

    def command_long_send(self, *args):
        self.sent.append(("command_long", args))

    def set_position_target_global_int_send(self, *args):
        self.sent.append(("set_position_target", args))


class FakeConn:
    def __init__(self):
        self.mav = FakeMav()
        self.target_system    = 1
        self.target_component = 1

    def close(self):
        pass


def make_adapter(messages=None):
    adapter = MAVLinkAdapter("udp:127.0.0.1:14550")
    adapter._conn  = FakeConn()
    adapter._cache = FakeCache(messages)
    return adapter


# ── Cached reads ──────────────────────────────────────────────────────────────

def test_get_telemetry_reads_the_cache(monkeypatch):
    adapter = make_adapter({
        "GLOBAL_POSITION_INT": FakeMsg("GLOBAL_POSITION_INT",
                                       relative_alt=12340, hdg=27100,
                                       vx=100, vy=0),
        "VFR_HUD": FakeMsg("VFR_HUD", airspeed=2.5, groundspeed=2.4),
    })

    result = adapter.execute("get_telemetry", {})

    assert result == {
        "altitude": 12.34, "airspeed": 2.5, "groundspeed": 2.4, "heading": 271.0,
    }
    assert adapter._cache.waits == []      # pure cache hit, no blocking wait


def test_get_telemetry_tolerates_missing_vfr_hud():
    """VFR_HUD is optional — it must never be waited on."""
    adapter = make_adapter({
        "GLOBAL_POSITION_INT": FakeMsg("GLOBAL_POSITION_INT",
                                       relative_alt=5000, hdg=9000, vx=300, vy=400),
    })

    result = adapter.execute("get_telemetry", {})

    assert result["altitude"] == 5.0
    assert result["groundspeed"] == 5.0    # derived from vx/vy
    assert "VFR_HUD" not in adapter._cache.waits


def test_unknown_heading_is_normalised():
    adapter = make_adapter({
        "GLOBAL_POSITION_INT": FakeMsg("GLOBAL_POSITION_INT",
                                       relative_alt=1000, hdg=65535, vx=0, vy=0),
    })
    assert adapter.execute("get_telemetry", {})["heading"] == 0.0


def test_get_position_str_reads_the_cache():
    adapter = make_adapter({
        "GLOBAL_POSITION_INT": FakeMsg("GLOBAL_POSITION_INT",
                                       lat=238103000, lon=904125000, relative_alt=5000),
    })
    result = adapter.execute("get_position_str", {})
    assert result["position"] == "Lat: 23.810300, Lon: 90.412500, Alt: 5.0m"


def test_get_battery_keeps_the_level_percent_key():
    adapter = make_adapter({
        "BATTERY_STATUS": FakeMsg("BATTERY_STATUS", voltages=[11800],
                                  current_battery=210, battery_remaining=78),
    })
    result = adapter.execute("get_battery", {})
    assert result["level_percent"] == 78.0   # safety_policy reads this exact key
    assert result["voltage"] == 11.8


def test_get_current_state_reads_cached_heartbeat():
    adapter = make_adapter({
        "HEARTBEAT": FakeMsg("HEARTBEAT", base_mode=0x80, custom_mode=4,
                             system_status=4),
    })
    result = adapter.execute("get_current_state", {})
    assert result == {"mode": "GUIDED", "armed": True, "system_status": "ACTIVE"}


# ── set_mode fast path ────────────────────────────────────────────────────────

def test_set_mode_is_a_noop_when_already_in_mode():
    """
    goto_position / takeoff / land all route through set_mode, and after
    takeoff the vehicle is already in GUIDED.  This used to send the command
    and then wait for the next 1 Hz heartbeat to confirm it.
    """
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=4)})

    result = adapter.execute("set_mode", {"mode": "GUIDED"})

    assert result == {"status": "ok", "mode": "GUIDED"}
    assert adapter._conn.mav.sent == []     # nothing was transmitted


def test_set_mode_sends_and_confirms_when_mode_differs():
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=5)})  # LOITER

    result = adapter.execute("set_mode", {"mode": "GUIDED"})

    assert result["error"].startswith("mode change to 'GUIDED' not confirmed")
    assert len(adapter._conn.mav.sent) == 1                    # command went out
    assert "HEARTBEAT" in adapter._cache.waits                 # confirmation waited


def test_set_mode_rejects_unknown_mode():
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=4)})
    result = adapter.execute("set_mode", {"mode": "WARP"})
    assert "unknown mode" in result["error"]
    assert adapter._conn.mav.sent == []


def test_goto_position_skips_the_mode_change_in_guided():
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=4)})

    result = adapter.execute("goto_position", {"lat": 23.81, "lon": 90.41, "alt": 10.0})

    assert result["status"] == "moving"
    kinds = [kind for kind, _ in adapter._conn.mav.sent]
    assert kinds == ["set_position_target"]   # no redundant DO_SET_MODE


# ── COMMAND_ACK correlation ───────────────────────────────────────────────────

def test_arm_matches_its_own_ack():
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=4)})
    adapter._cache.acks[400] = FakeMsg("COMMAND_ACK", command=400, result=0)

    assert adapter.execute("arm_drone", {}) == {"status": "armed"}


def test_arm_reports_a_rejected_ack():
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=4)})
    adapter._cache.acks[400] = FakeMsg("COMMAND_ACK", command=400, result=4)

    result = adapter.execute("arm_drone", {})
    assert "rejected (result=4)" in result["error"]


def test_missing_ack_is_an_error_not_an_exception():
    adapter = make_adapter({"HEARTBEAT": FakeMsg("HEARTBEAT", custom_mode=4)})
    result = adapter.execute("arm_drone", {})
    assert "no COMMAND_ACK received" in result["error"]


# ── Cache-polled waits ────────────────────────────────────────────────────────

def test_wait_altitude_returns_as_soon_as_the_cache_agrees():
    adapter = make_adapter({
        "GLOBAL_POSITION_INT": FakeMsg("GLOBAL_POSITION_INT", relative_alt=10000),
    })

    t0 = time.monotonic()
    result = adapter.execute("wait_altitude", {"target_alt": 10.0})
    elapsed = time.monotonic() - t0

    assert result == {"status": "altitude_reached", "altitude": 10.0}
    assert elapsed < 0.5      # the old loop paid a 2 s blocking recv per turn


def test_wait_altitude_times_out_without_blocking_forever():
    adapter = make_adapter({
        "GLOBAL_POSITION_INT": FakeMsg("GLOBAL_POSITION_INT", relative_alt=1000),
    })
    result = adapter.execute("wait_altitude", {"target_alt": 50.0, "timeout": 0.2})
    assert "timed out waiting for altitude" in result["error"]


def test_wait_arrival_needs_three_distinct_slow_samples():
    adapter = make_adapter({"VFR_HUD": FakeMsg("VFR_HUD", groundspeed=0.1)})
    # FakeCache stamps every read with a new timestamp, so each poll counts as
    # a fresh sample and three of them satisfy the arrival condition.
    assert adapter.execute("wait_arrival", {"timeout": 1.0}) == {"status": "arrived"}


def test_wait_arrival_times_out_while_still_moving():
    adapter = make_adapter({"VFR_HUD": FakeMsg("VFR_HUD", groundspeed=4.0)})
    result = adapter.execute("wait_arrival", {"timeout": 0.2})
    assert "timed out waiting for arrival" in result["error"]


# ── Disconnected behaviour ────────────────────────────────────────────────────

@pytest.mark.parametrize("tool,args", [
    ("set_mode",       {"mode": "GUIDED"}),
    ("goto_position",  {"lat": 1.0, "lon": 2.0, "alt": 3.0}),
    ("arm_drone",      {}),
    ("disarm_drone",   {}),
    ("takeoff",        {"altitude": 10.0}),
    ("set_speed",      {"speed_ms": 5.0}),
    ("set_yaw",        {"yaw_deg": 90.0}),
    ("wait_altitude",  {"target_alt": 5.0}),
    ("wait_arrival",   {}),
    ("get_telemetry",  {}),
    ("get_battery",    {}),
])
def test_handlers_report_an_error_instead_of_raising(tool, args):
    """
    An unhandled exception costs a dispatcher retry and an extra LLM round
    trip; a clean error dict costs neither.
    """
    adapter = MAVLinkAdapter("udp:127.0.0.1:14550")
    result = adapter.execute(tool, args)
    assert "error" in result
