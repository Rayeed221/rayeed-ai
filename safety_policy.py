import math
import time
import logging

from config import (
    BATTERY_CRITICAL_PCT, BATTERY_LOW_PCT,
    ALTITUDE_CEILING_M, MAX_SPEED_MS,
    TELEMETRY_STALE_SEC, EMERGENCY_STALE_SEC,
    MAX_RETRY_COUNT,
    GEOFENCE_ENABLED, GEOFENCE_MAX_RADIUS_M,
)
from schemas import ErrorSchema

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
        self._home_lat:        float | None = None
        self._home_lon:        float | None = None
        self._env_memory                    = None

    # ── Live value updates ────────────────────────────────────────────────────

    def update_telemetry_timestamp(self):
        self._last_tel_time = time.time()

    def update_battery(self, pct: float):
        self._last_battery = pct

    def update_altitude(self, alt_m: float):
        self._last_altitude = alt_m

    def set_home(self, lat: float, lon: float):
        self._home_lat = lat
        self._home_lon = lon
        logger.info(f"[SAFETY] Home position set: ({lat:.6f}, {lon:.6f})")

    def set_environment_memory(self, env_memory):
        self._env_memory = env_memory

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

    @staticmethod
    def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6_371_000.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def check_geofence(self, target_lat: float, target_lon: float) -> ErrorSchema | None:
        if not GEOFENCE_ENABLED or self._home_lat is None:
            return None

        dist = self._haversine_m(self._home_lat, self._home_lon, target_lat, target_lon)
        if dist > GEOFENCE_MAX_RADIUS_M:
            return ErrorSchema(
                code="GEOFENCE_BREACH",
                message=(
                    f"Target ({target_lat:.6f}, {target_lon:.6f}) is {dist:.1f}m from home "
                    f"— exceeds geofence radius {GEOFENCE_MAX_RADIUS_M}m"
                ),
                retryable=False,
                context={
                    "target_lat": target_lat,
                    "target_lon": target_lon,
                    "distance_m": round(dist, 1),
                    "max_radius_m": GEOFENCE_MAX_RADIUS_M,
                },
            )

        if self._env_memory is not None:
            for zone in self._env_memory.no_fly_zones():
                zone_dist = self._haversine_m(
                    zone["lat"], zone["lon"], target_lat, target_lon
                )
                if zone_dist <= zone["radius_m"]:
                    return ErrorSchema(
                        code="NO_FLY_ZONE",
                        message=(
                            f"Target is {zone_dist:.1f}m from no-fly zone "
                            f"'{zone.get('label', 'unnamed')}' (radius {zone['radius_m']}m)"
                        ),
                        retryable=False,
                        context={
                            "zone_label": zone.get("label", ""),
                            "zone_lat": zone["lat"],
                            "zone_lon": zone["lon"],
                            "zone_radius_m": zone["radius_m"],
                            "distance_m": round(zone_dist, 1),
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

        if tool_name == "goto_position":
            err = self.check_geofence(args.get("lat", 0.0), args.get("lon", 0.0))
            if err:
                return err

        # Retry limit
        err = self.check_retry_limit(tool_name)
        if err:
            return err

        return None
