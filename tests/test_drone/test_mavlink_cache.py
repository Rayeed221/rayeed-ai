"""
tests/test_drone/test_mavlink_cache.py — MAVLinkCache (latency blackboard).

The cache replaces per-handler blocking recv_match() calls, which discarded
every non-matching message while they waited and made concurrent consumers
steal each other's telemetry.  These tests use a fake connection, so they run
without pymavlink or hardware.
"""

import threading
import time

import pytest

from adapters.mavlink_cache import MAVLinkCache

from conftest import FakeConn, FakeMsg, wait_for as _wait_for


@pytest.fixture
def cache():
    conn = FakeConn()
    c = MAVLinkCache(conn)
    c._conn_for_test = conn          # convenience handle for the tests
    yield c
    c.stop()


# ── Reader lifecycle ──────────────────────────────────────────────────────────

def test_start_and_stop(cache):
    cache.start()
    assert cache.is_running() is True
    cache.stop()
    assert cache.is_running() is False


def test_start_is_idempotent(cache):
    cache.start()
    cache.start()
    assert cache.is_running() is True


def test_reader_survives_recv_exceptions():
    class Exploding(FakeConn):
        def recv_match(self, blocking=True, timeout=0.5, **kwargs):
            self.calls += 1
            if self.calls < 3:
                raise OSError("link dropped")
            return FakeMsg("HEARTBEAT", custom_mode=4)

    c = MAVLinkCache(Exploding())
    c.start()
    try:
        assert _wait_for(lambda: c.get("HEARTBEAT") is not None)
        assert c.stats()["errors"] >= 2
    finally:
        c.stop()


# ── Reads ─────────────────────────────────────────────────────────────────────

def test_get_returns_latest_message(cache):
    conn = cache._conn_for_test
    conn.push(FakeMsg("GLOBAL_POSITION_INT", relative_alt=1000))
    cache.start()
    assert _wait_for(lambda: cache.get("GLOBAL_POSITION_INT") is not None)

    conn.push(FakeMsg("GLOBAL_POSITION_INT", relative_alt=5000))
    assert _wait_for(lambda: cache.get("GLOBAL_POSITION_INT").relative_alt == 5000)


def test_get_unknown_type_is_none(cache):
    cache.start()
    assert cache.get("VFR_HUD") is None


def test_get_respects_max_age(cache):
    cache._conn_for_test.push(FakeMsg("VFR_HUD", groundspeed=0.1))
    cache.start()
    assert _wait_for(lambda: cache.get("VFR_HUD") is not None)

    time.sleep(0.05)
    assert cache.get("VFR_HUD", max_age=0.01) is None     # too old
    assert cache.get("VFR_HUD", max_age=10.0) is not None  # still cached


def test_bad_data_is_not_cached(cache):
    cache._conn_for_test.push(FakeMsg("BAD_DATA"))
    cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=4))
    cache.start()
    assert _wait_for(lambda: cache.get("HEARTBEAT") is not None)
    assert cache.get("BAD_DATA") is None


def test_source_system_drops_other_vehicles():
    """One cache holds ONE vehicle's state.  Our own avoidance layer emits GCS
    heartbeats on the same link, and caching one would corrupt mode detection."""
    conn = FakeConn([
        FakeMsg("HEARTBEAT", src_system=254, custom_mode=0),   # another GCS
        FakeMsg("HEARTBEAT", src_system=1,   custom_mode=4),   # the autopilot
    ])
    c = MAVLinkCache(conn, source_system=1)
    c.start()
    try:
        assert _wait_for(lambda: c.get("HEARTBEAT") is not None)
        time.sleep(0.05)
        assert c.get("HEARTBEAT").custom_mode == 4   # the foreign one never landed
    finally:
        c.stop()


def test_source_system_filters_every_type_not_just_heartbeat():
    conn = FakeConn([
        FakeMsg("GLOBAL_POSITION_INT", src_system=99, relative_alt=9999),
        FakeMsg("GLOBAL_POSITION_INT", src_system=1,  relative_alt=1000),
    ])
    c = MAVLinkCache(conn, source_system=1)
    c.start()
    try:
        assert _wait_for(lambda: c.get("GLOBAL_POSITION_INT") is not None)
        time.sleep(0.05)
        assert c.get("GLOBAL_POSITION_INT").relative_alt == 1000
    finally:
        c.stop()


def test_no_source_system_accepts_everything(cache):
    cache._conn_for_test.push(FakeMsg("HEARTBEAT", src_system=254, custom_mode=7))
    cache.start()
    assert _wait_for(lambda: cache.get("HEARTBEAT") is not None)


def test_get_with_ts_distinguishes_samples(cache):
    cache._conn_for_test.push(FakeMsg("VFR_HUD", groundspeed=0.2))
    cache.start()
    assert _wait_for(lambda: cache.get("VFR_HUD") is not None)
    _, first = cache.get_with_ts("VFR_HUD")

    cache._conn_for_test.push(FakeMsg("VFR_HUD", groundspeed=0.3))
    assert _wait_for(lambda: cache.get_with_ts("VFR_HUD")[1] != first)


def test_get_with_ts_reports_absence(cache):
    assert cache.get_with_ts("HEARTBEAT") == (None, None)
    cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=4))
    cache.start()
    assert _wait_for(lambda: cache.get("HEARTBEAT") is not None)
    _, ts = cache.get_with_ts("HEARTBEAT")
    assert time.monotonic() - ts < 1.0


# ── Waiting ───────────────────────────────────────────────────────────────────

def test_wait_returns_when_message_arrives(cache):
    cache.start()
    threading.Timer(
        0.05, lambda: cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=4))
    ).start()
    msg = cache.wait("HEARTBEAT", timeout=2.0)
    assert msg is not None and msg.custom_mode == 4


def test_wait_times_out_on_silence(cache):
    cache.start()
    t0 = time.monotonic()
    assert cache.wait("HEARTBEAT", timeout=0.1) is None
    assert time.monotonic() - t0 < 1.0


def test_wait_applies_match_predicate(cache):
    cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=5))   # LOITER
    cache.start()
    assert _wait_for(lambda: cache.get("HEARTBEAT") is not None)

    # Not yet in GUIDED — the predicate must reject the cached LOITER heartbeat
    assert cache.wait("HEARTBEAT", timeout=0.05,
                      match=lambda m: m.custom_mode == 4) is None

    cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=4))   # GUIDED
    assert cache.wait("HEARTBEAT", timeout=2.0,
                      match=lambda m: m.custom_mode == 4) is not None


# ── COMMAND_ACK correlation ───────────────────────────────────────────────────

def test_wait_ack_matches_command_id(cache):
    cache.start()
    since = time.monotonic()
    cache._conn_for_test.push(FakeMsg("COMMAND_ACK", command=400, result=0))
    ack = cache.wait_ack(400, since=since, timeout=2.0)
    assert ack is not None and ack.result == 0


def test_wait_ack_ignores_other_commands(cache):
    cache.start()
    since = time.monotonic()
    cache._conn_for_test.push(FakeMsg("COMMAND_ACK", command=176, result=0))
    assert cache.wait_ack(400, since=since, timeout=0.1) is None


def test_wait_ack_ignores_acks_older_than_the_send(cache):
    """A stale ACK from a previous command must never satisfy a new wait."""
    cache.start()
    cache._conn_for_test.push(FakeMsg("COMMAND_ACK", command=400, result=0))
    assert _wait_for(lambda: cache.wait_ack(400, since=0.0, timeout=0.05) is not None)

    later = time.monotonic()
    assert cache.wait_ack(400, since=later, timeout=0.1) is None


# ── Concurrency ───────────────────────────────────────────────────────────────

def test_concurrent_readers_do_not_steal_messages(cache):
    """
    The whole point of the cache: several consumers reading different message
    types at once must all see their data.  With blocking recv_match(type=X)
    each reader discarded the others' messages.
    """
    conn = cache._conn_for_test
    for msg in (
        FakeMsg("GLOBAL_POSITION_INT", relative_alt=3000),
        FakeMsg("VFR_HUD", groundspeed=1.5),
        FakeMsg("BATTERY_STATUS", battery_remaining=77),
    ):
        conn.push(msg)
    cache.start()

    results = {}

    def reader(msg_type):
        results[msg_type] = cache.wait(msg_type, timeout=2.0)

    threads = [
        threading.Thread(target=reader, args=(t,))
        for t in ("GLOBAL_POSITION_INT", "VFR_HUD", "BATTERY_STATUS")
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=3.0)

    assert results["GLOBAL_POSITION_INT"].relative_alt == 3000
    assert results["VFR_HUD"].groundspeed == 1.5
    assert results["BATTERY_STATUS"].battery_remaining == 77


def test_cached_read_is_fast(cache):
    """A cache hit must not cost a round trip — this is the latency claim."""
    cache._conn_for_test.push(FakeMsg("GLOBAL_POSITION_INT", relative_alt=2000))
    cache.start()
    assert _wait_for(lambda: cache.get("GLOBAL_POSITION_INT") is not None)

    t0 = time.monotonic()
    for _ in range(1000):
        cache.get("GLOBAL_POSITION_INT", max_age=10.0)
    assert (time.monotonic() - t0) < 0.5


def test_stats_reports_tracked_types(cache):
    cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=4))
    cache.start()
    assert _wait_for(lambda: cache.get("HEARTBEAT") is not None)
    stats = cache.stats()
    assert stats["running"] is True
    assert "HEARTBEAT" in stats["ages_sec"]


def test_wait_with_zero_timeout_checks_once_without_blocking(cache):
    """The adapter reads optional streams with timeout=0 — it must never block."""
    cache.start()
    t0 = time.monotonic()
    assert cache.wait("VFR_HUD", timeout=0.0) is None
    assert time.monotonic() - t0 < 0.1

    cache._conn_for_test.push(FakeMsg("VFR_HUD", groundspeed=1.0))
    assert _wait_for(lambda: cache.wait("VFR_HUD", timeout=0.0) is not None)


def test_waiter_wakes_on_arrival_not_on_a_poll_tick(cache):
    """Condition-based wait should return promptly once the message lands."""
    cache.start()
    threading.Timer(
        0.05, lambda: cache._conn_for_test.push(FakeMsg("SYS_STATUS", voltage_battery=11000))
    ).start()
    t0 = time.monotonic()
    msg = cache.wait("SYS_STATUS", timeout=2.0)
    assert msg is not None
    assert time.monotonic() - t0 < 0.5


def test_stop_releases_a_blocked_waiter(cache):
    cache.start()
    threading.Timer(0.05, cache.stop).start()
    t0 = time.monotonic()
    assert cache.wait("NEVER_ARRIVES", timeout=3.0) is None
    assert time.monotonic() - t0 < 3.0
