"""
Shared test doubles for the MAVLink layer.

`FakeMsg` and `wait_for` were duplicated across test_mavlink_cache.py and
test_mavlink_adapter_fastpath.py; they live here so the two files' helpers stay
interchangeable.
"""

import threading
import time

import pytest


class FakeMsg:
    """Stand-in for a pymavlink message: a type, a source system, and fields."""

    def __init__(self, msg_type: str = "HEARTBEAT", src_system: int = 1, **fields):
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

    def __init__(self, messages=None, target_system: int = 1):
        self._queue = list(messages or [])
        self._lock  = threading.Lock()
        self.calls  = 0
        self.target_system    = target_system
        self.target_component = 1

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

    def close(self):
        pass


def wait_for(predicate, timeout: float = 2.0) -> bool:
    """Poll `predicate` until true or `timeout` expires."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.005)
    return False


@pytest.fixture
def fake_msg():
    return FakeMsg
