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


# ── Fakes ─────────────────────────────────────────────────────────────────────

class FakeMsg:
    def __init__(self, msg_type: str, src_system: int = 1, **fields):
        self._type = msg_type
        self._src  = src_system
        for k, v in fields.items():
            setattr(self, k, v)

    def get_type(self):
        return self._type

    def get_srcSystem(self):
        return self._src


class FakeConn:
    """Hands out queued messages, then blocks like a quiet link would."""

    def __init__(self, messages=None):
        self._queue = list(messages or [])
        self._lock  = threading.Lock()
        self.calls  = 0

    def push(self, msg):
        with self._lock:
            self._queue.append(msg)

    def recv_match(self, blocking=True, timeout=0.5, **kwargs):
        self.calls += 1
        with self._lock:
            if self._queue:
                return self._queue.pop(0)
        time.sleep(min(timeout, 0.01))
        return None


@pytest.fixture
def cache():
    conn = FakeConn()
    c = MAVLinkCache(conn, poll_interval=0.001)
    c._conn_for_test = conn          # convenience handle for the tests
    yield c
    c.stop()


def _wait_for(predicate, timeout=2.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return False


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

    c = MAVLinkCache(Exploding(), poll_interval=0.001)
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


def test_msg_filter_drops_rejected_messages():
    conn = FakeConn([
        FakeMsg("HEARTBEAT", src_system=254, custom_mode=0),   # another GCS
        FakeMsg("HEARTBEAT", src_system=1,   custom_mode=4),   # the autopilot
    ])
    c = MAVLinkCache(
        conn, poll_interval=0.001,
        msg_filter=lambda m: m.get_srcSystem() == 1,
    )
    c.start()
    try:
        assert _wait_for(lambda: c.get("HEARTBEAT") is not None)
        time.sleep(0.05)
        assert c.get("HEARTBEAT").custom_mode == 4   # the foreign one never landed
    finally:
        c.stop()


def test_get_with_ts_distinguishes_samples(cache):
    cache._conn_for_test.push(FakeMsg("VFR_HUD", groundspeed=0.2))
    cache.start()
    assert _wait_for(lambda: cache.get("VFR_HUD") is not None)
    _, first = cache.get_with_ts("VFR_HUD")

    cache._conn_for_test.push(FakeMsg("VFR_HUD", groundspeed=0.3))
    assert _wait_for(lambda: cache.get_with_ts("VFR_HUD")[1] != first)


def test_age_tracks_last_seen(cache):
    assert cache.age("HEARTBEAT") is None
    cache._conn_for_test.push(FakeMsg("HEARTBEAT", custom_mode=4))
    cache.start()
    assert _wait_for(lambda: cache.age("HEARTBEAT") is not None)
    assert cache.age("HEARTBEAT") < 1.0


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
