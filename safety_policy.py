import math
import time
import logging
from typing import TYPE_CHECKING, Optional

from config import (
    BATTERY_CRITICAL_PCT, BATTERY_LOW_PCT,
    ALTITUDE_CEILING_M, MAX_SPEED_MS,
    TELEMETRY_STALE_SEC, EMERGENCY_STALE_SEC,
    MAX_RETRY_COUNT,
    AVOIDANCE_COLLISION_THR, AVOIDANCE_STALE_SEC,
    VIOSLAM_STALE_SEC, VIOSLAM_PROXIMITY_THR_M,
)
from schemas import ErrorSchema

if TYPE_CHECKING:
    from vision.avoidance.dronet_runner import DroNetRunner
    from localization.vio_slam.vio_slam_runner import VIOSLAMRunner

# Tools gated by the avoidance layer — position/speed commands conflict with
# DroNet's autonomous velocity steering in GUIDED mode.  The same set applies
# to the SLAM-proximity gate.
_AVOIDANCE_GATED: frozenset = frozenset({"goto_position", "set_speed"})


def _quat_forward(qw: float, qx: float, qy: float, qz: float) -> tuple:
    """Unit forward vector (camera Z axis) from a quaternion."""
    fx = 2.0 * (qx * qz + qw * qy)
    fy = 2.0 * (qy * qz - qw * qx)
    fz = 1.0 - 2.0 * (qx * qx + qy * qy)
    norm = math.sqrt(fx * fx + fy * fy + fz * fz)
    if norm < 1e-9:
        return (1.0, 0.0, 0.0)
    return (fx / norm, fy / norm, fz / norm)

logger = logging.getLogger(__name__)


class SafetyViolation(Exception):
    def __init__(self, error: ErrorSchema):
        self.error = error
        super().__init__(error.message)


class SafetyPolicy:
    def __init__(self, state_machine):
        self._sm               = state_machine
        self._retry_counts:    dict  = {}
        self._last_tel_time:   float = 0.0
        self._last_battery:    float = 100.0
        self._last_altitude:   float = 0.0
        self._avoidance_runner: Optional["DroNetRunner"]   = None
        self._vioslam_runner:   Optional["VIOSLAMRunner"]  = None

    # ── Avoidance state ───────────────────────────────────────────────────────

    def set_avoidance_runner(self, runner: "DroNetRunner") -> None:
        self._avoidance_runner = runner

    def get_avoidance_state(self):
        if self._avoidance_runner is not None:
            return self._avoidance_runner.get_state()
        return None

    # ── VIO/SLAM state ────────────────────────────────────────────────────────

    def set_vioslam_runner(self, runner: "VIOSLAMRunner") -> None:
        self._vioslam_runner = runner

    def get_vioslam_pose(self):
        if self._vioslam_runner is not None:
            return self._vioslam_runner.get_pose()
        return None

    def get_vioslam_snapshot(self):
        if self._vioslam_runner is not None:
            return self._vioslam_runner.get_snapshot()
        return None

    def check_slam_proximity(self, tool: str) -> tuple:
        """Block goto_position / set_speed if SLAM grid shows obstacle within
        VIOSLAM_PROXIMITY_THR_M of the drone's current forward vector."""
        if tool not in _AVOIDANCE_GATED or self._vioslam_runner is None:
            return True, ""
        pose = self._vioslam_runner.get_pose()
        if pose is None:
            return True, ""
        if (time.monotonic() - pose.timestamp) > VIOSLAM_STALE_SEC:
            return True, ""
        grid = self._vioslam_runner.get_occupancy_grid()
        fwd = _quat_forward(pose.qw, pose.qx, pose.qy, pose.qz)
        dist = grid.nearest_obstacle_along(
            (pose.x, pose.y, pose.z), fwd,
            max_dist_m=VIOSLAM_PROXIMITY_THR_M * 2.0,
        )
        if dist is not None and dist < VIOSLAM_PROXIMITY_THR_M:
            return False, f"SLAM obstacle at {dist:.2f}m < {VIOSLAM_PROXIMITY_THR_M}m"
        return True, ""

    def check_avoidance(self, tool: str) -> tuple:
        if tool not in _AVOIDANCE_GATED:
            return True, ""
        state = self.get_avoidance_state()
        if state is None:
            return True, ""
        age = time.monotonic() - state.timestamp
        if age > AVOIDANCE_STALE_SEC:
            return True, ""
        if state.collision_prob >= AVOIDANCE_COLLISION_THR:
            return False, (
                f"obstacle: prob={state.collision_prob:.2f} "
                f"depth={state.depth_mm:.0f}mm — avoidance active"
            )
        return True, ""

    # ── Live value updates ────────────────────────────────────────────────────

    def update_telemetry_timestamp(self):
        self._last_tel_time = time.time()

    def update_battery(self, pct: float):
        self._last_battery = pct

    def update_altitude(self, alt_m: float):
        self._last_altitude = alt_m

    # ── Individual checks ─────────────────────────────────────────────────────

    def check_telemetry_freshness(self) -> ErrorSchema | None:
        if self._last_tel_time == 0.0:
            return None  # telemetry not yet started
        age = time.time() - self._last_tel_time
        if age > EMERGENCY_STALE_SEC:
            return ErrorSchema(
                code="TELEMETRY_EMERGENCY",
                message=f"Telemetry stale {age:.1f}s — exceeds emergency threshold {EMERGENCY_STALE_SEC}s",
                retryable=False,
                context={"age_sec": age, "threshold": EMERGENCY_STALE_SEC},
            )
        if age > TELEMETRY_STALE_SEC:
            return ErrorSchema(
                code="TELEMETRY_STALE",
                message=f"Telemetry stale {age:.1f}s — planner wait required",
                retryable=True,
                context={"age_sec": age, "threshold": TELEMETRY_STALE_SEC},
            )
        return None

    def check_battery(self) -> ErrorSchema | None:
        pct = self._last_battery
        if pct <= BATTERY_CRITICAL_PCT:
            return ErrorSchema(
                code="BATTERY_CRITICAL",
                message=f"Battery {pct}% ≤ critical threshold {BATTERY_CRITICAL_PCT}%",
                retryable=False,
                context={"battery_pct": pct},
            )
        if pct <= BATTERY_LOW_PCT:
            return ErrorSchema(
                code="BATTERY_LOW",
                message=f"Battery {pct}% ≤ low threshold {BATTERY_LOW_PCT}%",
                retryable=True,
                context={"battery_pct": pct},
            )
        return None

    def check_altitude(self, target_alt: float = None) -> ErrorSchema | None:
        alt = target_alt if target_alt is not None else self._last_altitude
        if alt > ALTITUDE_CEILING_M:
            return ErrorSchema(
                code="ALTITUDE_CEILING",
                message=f"Altitude {alt}m exceeds ceiling {ALTITUDE_CEILING_M}m",
                retryable=False,
                context={"requested_alt": alt, "ceiling": ALTITUDE_CEILING_M},
            )
        return None

    def check_speed(self, speed_ms: float) -> ErrorSchema | None:
        if speed_ms > MAX_SPEED_MS:
            return ErrorSchema(
                code="SPEED_EXCEEDED",
                message=f"Speed {speed_ms} m/s exceeds max {MAX_SPEED_MS} m/s",
                retryable=False,
                context={"requested": speed_ms, "max": MAX_SPEED_MS},
            )
        return None

    def check_command_legality(self, tool_name: str, current_state) -> ErrorSchema | None:
        from tool_registry import TOOL_REGISTRY  # local to avoid circular import
        meta = TOOL_REGISTRY.get(tool_name)
        if not meta:
            return ErrorSchema(
                code="UNKNOWN_TOOL",
                message=f"Tool '{tool_name}' not in registry",
                retryable=False,
                context={"tool": tool_name},
            )
        allowed = meta.get("allowed_states")
        if allowed is not None and current_state not in allowed:
            return ErrorSchema(
                code="ILLEGAL_COMMAND",
                message=f"'{tool_name}' not allowed in state '{current_state.value}'",
                retryable=False,
                context={
                    "tool": tool_name,
                    "state": current_state.value,
                    "allowed": [s.value for s in allowed],
                },
            )
        return None

    # ── Retry management ──────────────────────────────────────────────────────

    def increment_retry(self, tool: str) -> int:
        self._retry_counts[tool] = self._retry_counts.get(tool, 0) + 1
        return self._retry_counts[tool]

    def reset_retry(self, tool: str):
        self._retry_counts.pop(tool, None)

    def check_retry_limit(self, tool: str) -> ErrorSchema | None:
        count = self._retry_counts.get(tool, 0)
        if count >= MAX_RETRY_COUNT:
            return ErrorSchema(
                code="MAX_RETRIES",
                message=f"'{tool}' failed {count}× — max {MAX_RETRY_COUNT} reached",
                retryable=False,
                context={"tool": tool, "count": count},
            )
        return None

    # ── Full pre-execution gate ────────────────────────────────────────────────

    def pre_execute_check(self, tool_name: str, args: dict) -> ErrorSchema | None:
        """Run all checks before a tool is executed. Returns first blocking error."""

        # Telemetry freshness (non-retryable stale → block)
        err = self.check_telemetry_freshness()
        if err and not err.retryable:
            return err

        # Battery (non-retryable critical → block)
        err = self.check_battery()
        if err and not err.retryable:
            return err

        # Command legality (state gate)
        err = self.check_command_legality(tool_name, self._sm.state)
        if err:
            return err

        # Tool-specific argument checks
        if tool_name == "takeoff":
            err = self.check_altitude(target_alt=args.get("altitude", 0))
            if err:
                return err

        if tool_name == "set_speed":
            err = self.check_speed(args.get("speed_ms", 0))
            if err:
                return err

        # Avoidance gate — block position/speed commands during active obstacle steering
        ok, msg = self.check_avoidance(tool_name)
        if not ok:
            return ErrorSchema(
                code="AVOIDANCE_ACTIVE",
                message=msg,
                retryable=True,
                context={"tool": tool_name},
            )

        # SLAM proximity gate — block position/speed commands when the SLAM
        # occupancy grid shows an obstacle within VIOSLAM_PROXIMITY_THR_M
        # of the drone's current forward vector.
        ok, msg = self.check_slam_proximity(tool_name)
        if not ok:
            return ErrorSchema(
                code="SLAM_PROXIMITY",
                message=msg,
                retryable=True,
                context={"tool": tool_name},
            )

        # Retry limit
        err = self.check_retry_limit(tool_name)
        if err:
            return err

        return None
