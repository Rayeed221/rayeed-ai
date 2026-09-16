"""
MAVLinkCache — single-reader message blackboard for the MAVLink link.

Why this exists (latency):
    ``mavutil.recv_match(type=X, blocking=True)`` *discards* every message that
    is not X while it waits.  The app has four independent consumers of one
    connection (TelemetryReader @2 Hz, PositionMonitor @5 s, BatteryMonitor
    @10 s, and every LLM tool call), each running in its own
    ``asyncio.to_thread`` worker.  They steal each other's messages, so a
    ``get_telemetry`` that should cost ~0 ms drifts toward its 5 s timeout.
    pymavlink connections are also not thread-safe.

    The fix is the classic blackboard: ONE reader thread owns the socket,
    drains it continuously, and stores the latest message of each type.
    Handlers then read state in O(1) instead of issuing a blocking request.
    This is the "STATE" primitive of the drone grammar — a value that is
    always current, not a round trip that must be paid for.

Scope:
    One cache holds ONE vehicle's state.  ``source_system`` drops traffic from
    anything else on the link — other GCS clients, including our own avoidance
    layer, emit heartbeats that would otherwise corrupt mode detection.

Thread safety:
    ``get`` / ``get_with_ts`` / ``wait`` / ``wait_ack`` are safe from any
    thread.  Sends stay in the adapter, serialised by its own lock.
"""

import logging
import threading
import time
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# recv_match() timeout inside the reader loop.  Short enough that stop() is
# responsive, long enough that an idle link does not spin the CPU.
_RECV_TIMEOUT = 0.5


class MAVLinkCache:
    """Latest-message-per-type cache fed by one background reader thread."""

    def __init__(self, conn, source_system: Optional[int] = None):
        self._conn = conn
        # Accept only this system's traffic.  None = accept everything (tests).
        self._source_system = source_system
        # Waiters block on this condition instead of polling, so an idle link
        # costs zero wakeups and a waiter fires the instant its message lands.
        self._cond = threading.Condition()
        self._latest: dict = {}   # msg_type -> (msg, monotonic_ts)
        self._acks:   dict = {}   # command_id -> (msg, monotonic_ts)
        self._thread: Optional[threading.Thread] = None
        self._stop    = threading.Event()
        self._errors  = 0

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, name="mavlink_cache_reader", daemon=True
        )
        self._thread.start()
        logger.info("[MAVCACHE] Reader thread started")

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        with self._cond:
            self._cond.notify_all()   # release any waiter immediately
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None
        logger.info("[MAVCACHE] Reader thread stopped")

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    # ── Reader loop ──────────────────────────────────────────────────────────

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                msg = self._conn.recv_match(blocking=True, timeout=_RECV_TIMEOUT)
            except Exception as exc:
                self._errors += 1
                if self._errors <= 3 or self._errors % 100 == 0:
                    logger.warning(f"[MAVCACHE] recv_match failed ({self._errors}×): {exc}")
                time.sleep(0.1)
                continue

            if msg is None:
                continue

            try:
                msg_type = msg.get_type()
                if msg_type == "BAD_DATA":
                    continue
                if (self._source_system is not None
                        and msg.get_srcSystem() != self._source_system):
                    continue
            except Exception:
                continue

            now = time.monotonic()
            with self._cond:
                self._latest[msg_type] = (msg, now)
                if msg_type == "COMMAND_ACK":
                    # Keyed by command so a slow ACK cannot be mistaken for
                    # the ACK of a later, different command.
                    self._acks[getattr(msg, "command", -1)] = (msg, now)
                self._cond.notify_all()

    # ── Reads ────────────────────────────────────────────────────────────────

    def get_with_ts(self, msg_type: str, max_age: Optional[float] = None):
        """``(msg, monotonic_ts)`` for the latest message, or ``(None, None)``.

        The one read primitive — everything else is built on it.  Use this over
        ``get`` when the caller must tell one sample apart from the next (e.g.
        counting consecutive readings).
        """
        with self._cond:
            entry = self._latest.get(msg_type)
        if entry is None:
            return None, None
        msg, ts = entry
        if max_age is not None and (time.monotonic() - ts) > max_age:
            return None, None
        return msg, ts

    def get(self, msg_type: str, max_age: Optional[float] = None):
        """Latest cached message of this type, or None if absent/too old."""
        return self.get_with_ts(msg_type, max_age)[0]

    def wait(
        self,
        msg_type: str,
        timeout: float = 5.0,
        max_age: Optional[float] = None,
        match: Optional[Callable] = None,
    ):
        """
        Return a cached message satisfying the constraints, waiting if needed.

        Never touches the socket, so it cannot consume a message another caller
        is waiting for.  ``timeout=0`` checks the cache once without blocking.
        Returns None on timeout.
        """
        return self._wait_until(
            lambda: self._match_latest(msg_type, max_age, match), timeout
        )

    def wait_ack(self, command: int, since: float, timeout: float = 10.0):
        """
        Wait for a COMMAND_ACK for `command` that arrived after `since`
        (a ``time.monotonic()`` stamp taken just before the send).
        Returns the message, or None on timeout.
        """
        return self._wait_until(lambda: self._match_ack(command, since), timeout)

    # ── Internals ────────────────────────────────────────────────────────────

    def _match_latest(self, msg_type: str, max_age, match):
        """Caller must hold ``self._cond``."""
        entry = self._latest.get(msg_type)
        if entry is None:
            return None
        msg, ts = entry
        if max_age is not None and (time.monotonic() - ts) > max_age:
            return None
        if match is not None and not match(msg):
            return None
        return msg

    def _match_ack(self, command: int, since: float):
        """Caller must hold ``self._cond``."""
        entry = self._acks.get(command)
        if entry is not None and entry[1] >= since:
            return entry[0]
        return None

    def _wait_until(self, predicate: Callable, timeout: float):
        """
        Block until `predicate()` returns a non-None value or `timeout` expires.

        The predicate is evaluated under the lock and re-run only when the
        reader thread stores a new message, so a stale cached value is never
        re-tested in a spin.
        """
        deadline = time.monotonic() + timeout
        with self._cond:
            while True:
                found = predicate()
                if found is not None:
                    return found
                if self._stop.is_set():
                    # The reader is gone, so no message can still arrive —
                    # otherwise a long wait (wait_arrival budgets 120 s) would
                    # hold up shutdown for its full timeout.
                    return None
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return None
                self._cond.wait(remaining)

    # ── Diagnostics ──────────────────────────────────────────────────────────

    def stats(self) -> dict:
        now = time.monotonic()
        with self._cond:
            ages = {t: round(now - ts, 3) for t, (_, ts) in self._latest.items()}
        return {"running": self.is_running(), "errors": self._errors, "ages_sec": ages}
