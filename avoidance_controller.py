"""
AvoidanceController — 10 Hz closed-loop reactive obstacle avoidance.

Architecture:
  ┌──────────────────────────────────────────────────────────┐
  │  tool_dispatcher.goto_position(lat, lon, alt)            │
  │            ↓ set_goal()                                  │
  │  AvoidanceController (this module)                       │
  │   ├─ _control_loop  (10 Hz) — GRU → NED setpoints       │
  │   ├─ _telemetry_loop (50 Hz) — LOCAL_POSITION_NED/ATTITUDE│
  │   ├─ _heartbeat_loop (1 Hz) — GCS failsafe prevention   │
  │   └─ _watchdog_loop  (2 Hz) — liveness + NaN detection  │
  │            ↓ SET_POSITION_TARGET_LOCAL_NED (single writer)│
  │  ArduCopter FCU                                          │
  └──────────────────────────────────────────────────────────┘

Single-writer contract:
  While avoidance is active, ONLY this class publishes
  SET_POSITION_TARGET_LOCAL_NED. MAVLinkAdapter._handle_goto_position()
  is bypassed entirely via the tool_dispatcher intercept.

Threading model:
  All methods are async and run in the main asyncio event loop.
  Blocking pymavlink calls are wrapped with asyncio.to_thread().

GRU hidden state lifecycle:
  Reset to zeros:   set_goal() (new navigation target), NaN/Inf correction output
  Reset only:       correction magnitude > _DIVERGENCE_THRESHOLD_M
  Persists across:  every 10 Hz control cycle within the same goal

IMU note:
  OAK-D Lite has BMI270 (6-axis: accel + gyro only, NO magnetometer).
  Attitude quaternion comes from ArduCopter ATTITUDE message (EKF3 fusion),
  NOT from on-device IMU fusion — ArduCopter's estimate is strictly superior.
"""

import asyncio
import logging
import math
import time
from typing import List, Optional

import numpy as np

from config import (
    AVOIDANCE_HZ,
    AVOIDANCE_MAX_LATERAL_M,
    AVOIDANCE_MAX_VERTICAL_M,
    AVOIDANCE_SUB_GOAL_SPACING_M,
    AVOIDANCE_ARRIVAL_THRESHOLD_M,
)

logger = logging.getLogger(__name__)

# ── Timing constants ──────────────────────────────────────────────────────────
_CONTROL_PERIOD_S  = 1.0 / AVOIDANCE_HZ   # 0.1 s at 10 Hz
_TELEMETRY_PERIOD  = 0.02                   # 50 Hz
_HEARTBEAT_PERIOD  = 1.0                    # 1 Hz
_WATCHDOG_PERIOD   = 0.5                    # 2 Hz

# ── Safety thresholds ─────────────────────────────────────────────────────────
_FRAME_TIMEOUT_S        = 0.5    # OAK-D frame gap before disabling avoidance
_STALL_TIMEOUT_S        = 1.0    # control loop must fire within this window
_DIVERGENCE_THRESHOLD_M = 10.0   # GRU correction magnitude → reset hidden state

# ── MAVLink type_mask: position + velocity active, accel/yaw/yaw_rate ignored ─
# Bits 0-2 (pos) + bits 3-5 (vel) active; rest ignored
_POS_VEL_TYPE_MASK = 0b0000110111000000

# ── MAVLink frame / type constants (inline to avoid import-time pymavlink dep) ─
_MAV_FRAME_LOCAL_NED         = 1
_MAV_TYPE_ONBOARD_CONTROLLER = 18
_MAV_AUTOPILOT_INVALID       = 8


class AvoidanceController:
    """Reactive obstacle avoidance layer sitting between dispatcher and MAVLink."""

    def __init__(self, master, safety_policy, gru_session, oak_device):
        """
        Args:
            master:        pymavlink MAVLink connection (MAVLinkAdapter._conn)
            safety_policy: SafetyPolicy instance (altitude/battery gate reads)
            gru_session:   onnxruntime.InferenceSession for gru_avoidance.onnx
            oak_device:    depthai.Device instance (already started)
        """
        self._master       = master
        self._safety       = safety_policy
        self._gru          = gru_session
        self._oak          = oak_device

        # EKF origin (set in start() from HOME_POSITION message)
        self._origin_lat: float = 0.0
        self._origin_lon: float = 0.0
        self._origin_alt: float = 0.0

        # Current flight state (updated by _telemetry_loop)
        self._pos_ned: np.ndarray       = np.zeros(3, dtype=np.float32)
        self._vel_ned: np.ndarray       = np.zeros(3, dtype=np.float32)
        self._yaw_rad: float            = 0.0
        self._attitude_quat: np.ndarray = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)

        # Latest BMI270 IMU reading [ax, ay, az, gx, gy, gz]
        self._latest_imu: np.ndarray = np.zeros(6, dtype=np.float32)

        # GRU hidden state: [num_layers=1, batch=1, hidden=128]
        self._h: np.ndarray = np.zeros((1, 1, 128), dtype=np.float32)

        # Sub-goal navigation
        self._sub_goals: List[np.ndarray]    = []
        self._current_sub_idx: int           = 0
        self._goal_ned: Optional[np.ndarray] = None
        self._prev_sub_goal: np.ndarray      = np.zeros(3, dtype=np.float32)

        # Controller state
        self._avoidance_enabled: bool = True
        self._running: bool           = False

        # asyncio.Event created in start() for Python 3.10+ compatibility
        self._goal_event: Optional[asyncio.Event] = None

        # Watchdog timestamps
        self._last_control_time: float = 0.0
        self._last_frame_time:   float = 0.0

    # ── Startup ───────────────────────────────────────────────────────────────

    async def start(self) -> None:
        """
        Fetch EKF origin, request telemetry streams, launch 4 background tasks.
        Must be called after the MAVLink connection is established.
        """
        # Create asyncio.Event within the running loop (required for Python 3.10+)
        self._goal_event = asyncio.Event()

        # Fetch HOME_POSITION for NED origin
        home = await asyncio.to_thread(
            self._master.recv_match,
            type="HOME_POSITION",
            blocking=True,
            timeout=10.0,
        )
        if home is None:
            raise RuntimeError(
                "AvoidanceController: HOME_POSITION not received within 10 s — "
                "ensure ArduCopter has GPS fix and EKF is healthy"
            )

        self._origin_lat = home.latitude  / 1e7
        self._origin_lon = home.longitude / 1e7
        self._origin_alt = home.altitude  / 1000.0   # mm → m MSL
        logger.info(
            f"[AVOID] EKF origin: {self._origin_lat:.6f}, "
            f"{self._origin_lon:.6f}, alt={self._origin_alt:.1f} m MSL"
        )

        # Request LOCAL_POSITION_NED (id=32) and ATTITUDE (id=30) at 50 Hz
        await asyncio.to_thread(self._request_message_intervals)

        self._running = True

        # Launch 4 concurrent background tasks
        asyncio.create_task(self._control_loop(),   name="avoid_control")
        asyncio.create_task(self._telemetry_loop(), name="avoid_telemetry")
        asyncio.create_task(self._heartbeat_loop(), name="avoid_heartbeat")
        asyncio.create_task(self._watchdog_loop(),  name="avoid_watchdog")

        logger.info("[AVOID] Controller started — 4 tasks running")

    def _request_message_intervals(self) -> None:
        """Request LOCAL_POSITION_NED + ATTITUDE at 50 Hz via MAV_CMD_SET_MESSAGE_INTERVAL."""
        # MAV_CMD_SET_MESSAGE_INTERVAL = 511
        for msg_id, interval_us in [(32, 20_000), (30, 20_000)]:
            self._master.mav.command_long_send(
                self._master.target_system,
                self._master.target_component,
                511, 0,
                float(msg_id),
                float(interval_us),
                0, 0, 0, 0, 0,
            )

    # ── Goal management ───────────────────────────────────────────────────────

    async def set_goal(self, lat: float, lon: float, alt_msl: float) -> None:
        """
        Set new navigation goal. Converts GPS to NED, decomposes into sub-goals,
        resets GRU hidden state. Thread-safe for asyncio.

        Args:
            lat:     target latitude (degrees)
            lon:     target longitude (degrees)
            alt_msl: target altitude MSL (meters)
        """
        goal_ned = self._gps_to_ned(lat, lon, alt_msl)

        self._goal_ned        = goal_ned
        self._sub_goals       = self._decompose_path(self._pos_ned, goal_ned)
        self._current_sub_idx = 0
        self._prev_sub_goal   = self._pos_ned.copy()

        # Reset GRU hidden state — old context irrelevant for new trajectory
        self._h = np.zeros((1, 1, 128), dtype=np.float32)

        if self._goal_event is not None:
            self._goal_event.set()

        logger.info(
            f"[AVOID] Goal → NED={goal_ned}, "
            f"{len(self._sub_goals)} sub-goals @ "
            f"{AVOIDANCE_SUB_GOAL_SPACING_M} m spacing"
        )

    async def wait_for_arrival(self, timeout: float = 120.0) -> bool:
        """
        Poll until within AVOIDANCE_ARRIVAL_THRESHOLD_M of final goal, or timeout.

        Args:
            timeout: maximum seconds to wait

        Returns:
            True if arrived, False if timeout
        """
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            if self._goal_ned is not None:
                dist = float(np.linalg.norm(self._pos_ned - self._goal_ned))
                if dist <= AVOIDANCE_ARRIVAL_THRESHOLD_M:
                    logger.info(f"[AVOID] Arrived (dist={dist:.2f} m)")
                    self._goal_ned = None
                    if self._goal_event is not None:
                        self._goal_event.clear()
                    return True
            await asyncio.sleep(0.2)

        logger.warning(f"[AVOID] wait_for_arrival timeout after {timeout:.0f} s")
        return False

    # ── Control loop (10 Hz) ──────────────────────────────────────────────────

    async def _control_loop(self) -> None:
        while self._running:
            t_start = time.monotonic()

            if self._goal_event is None or not self._goal_event.is_set():
                await asyncio.sleep(_CONTROL_PERIOD_S)
                continue

            self._last_control_time = time.monotonic()

            try:
                await self._control_step()
            except Exception as exc:
                logger.error(f"[AVOID] Control step exception: {exc}", exc_info=True)

            elapsed = time.monotonic() - t_start
            await asyncio.sleep(max(0.0, _CONTROL_PERIOD_S - elapsed))

    async def _control_step(self) -> None:
        """One 10 Hz control iteration."""
        if not self._sub_goals:
            return

        # ── 1. Advance sub-goal when drone arrives within threshold ───────────
        if self._current_sub_idx < len(self._sub_goals):
            sub_goal = self._sub_goals[self._current_sub_idx]
            if np.linalg.norm(self._pos_ned - sub_goal) <= AVOIDANCE_ARRIVAL_THRESHOLD_M:
                self._prev_sub_goal   = sub_goal.copy()
                self._current_sub_idx += 1

        if self._current_sub_idx >= len(self._sub_goals):
            return  # All sub-goals reached; wait_for_arrival handles final check

        sub_goal = self._sub_goals[self._current_sub_idx]

        # ── 2. Encoder output from OAK-D (non-blocking) ───────────────────────
        depth_feat = self._get_encoder_output()  # [64] float32

        # ── 3. Assemble 80-D GRU input ────────────────────────────────────────
        goal_offset_raw = (self._goal_ned - self._pos_ned) if self._goal_ned is not None \
                          else (sub_goal - self._pos_ned)
        goal_norm  = goal_offset_raw / 50.0           # normalise by 50 m

        state_vec = np.concatenate([
            depth_feat,           # [64]
            self._latest_imu,     # [6]
            self._vel_ned,        # [3]
            self._attitude_quat,  # [4]
            goal_norm,            # [3]
        ]).astype(np.float32)     # [80]

        # ── 4. GRU inference (ONNX Runtime, RPi5 CPU) ─────────────────────────
        x_in = state_vec.reshape(1, 1, 80)
        try:
            outputs = self._gru.run(
                ["correction", "h_out"],
                {"x": x_in, "h_in": self._h},
            )
            correction_body = outputs[0].reshape(3)  # [3] in body frame
            h_new           = outputs[1]             # [1, 1, 128]
        except Exception as exc:
            logger.error(f"[AVOID] GRU inference failed: {exc}")
            correction_body = np.zeros(3, dtype=np.float32)
            h_new = self._h

        # ── 5. Validate GRU output ────────────────────────────────────────────
        if not np.all(np.isfinite(correction_body)):
            logger.warning("[AVOID] GRU output NaN/Inf — disabling avoidance, resetting hidden")
            self._avoidance_enabled = False
            self._h = np.zeros((1, 1, 128), dtype=np.float32)
            correction_body = np.zeros(3, dtype=np.float32)
        else:
            magnitude = float(np.linalg.norm(correction_body))
            if magnitude > _DIVERGENCE_THRESHOLD_M:
                logger.warning(
                    f"[AVOID] Correction divergence ({magnitude:.1f} m) — "
                    "resetting hidden state only"
                )
                self._h = np.zeros((1, 1, 128), dtype=np.float32)
                correction_body = np.zeros(3, dtype=np.float32)
            else:
                self._h = h_new

        # ── 6. Body → NED rotation (yaw-only, sufficient for level flight) ────
        correction_ned = self._body_to_ned(correction_body, self._yaw_rad)

        # ── 7. Line-constrained clamp (±lateral, ±vertical from path) ─────────
        if self._avoidance_enabled:
            correction_ned = self._apply_line_constrained_correction(
                sub_goal, self._prev_sub_goal, correction_ned
            )
        else:
            correction_ned = np.zeros(3, dtype=np.float32)

        # ── 8. Final target NED = sub-goal + avoidance correction ─────────────
        target_ned = sub_goal + correction_ned

        # Feed-forward velocity toward sub-goal (proportional, capped at 2 m/s)
        to_sub = sub_goal - self._pos_ned
        dist   = float(np.linalg.norm(to_sub))
        vel_ff = (to_sub / dist) * min(dist * 0.5, 2.0) if dist > 0.01 \
                 else np.zeros(3, dtype=np.float32)

        # ── 9. Publish (single writer) ────────────────────────────────────────
        await asyncio.to_thread(self._publish_position, target_ned, vel_ff)

    def _get_encoder_output(self) -> np.ndarray:
        """
        Pull latest encoder feature vector from OAK-D XLinkOut queue.
        Non-blocking (tryGet). Returns zeros if no frame available.
        Updates _last_frame_time for watchdog.
        """
        try:
            queue = self._oak.getOutputQueue("nn_out", maxSize=1, blocking=False)
            data  = queue.tryGet()
            if data is None:
                return np.zeros(64, dtype=np.float32)
            self._last_frame_time = time.monotonic()
            feat = np.array(data.getFirstLayerFp16(), dtype=np.float32)  # [64]
            return feat
        except Exception as exc:
            logger.debug(f"[AVOID] Encoder output read: {exc}")
            return np.zeros(64, dtype=np.float32)

    # ── Telemetry loop (50 Hz) ────────────────────────────────────────────────

    async def _telemetry_loop(self) -> None:
        while self._running:
            t_start = time.monotonic()
            try:
                # LOCAL_POSITION_NED — position + velocity in NED frame
                pos_msg = await asyncio.to_thread(
                    self._master.recv_match,
                    type="LOCAL_POSITION_NED",
                    blocking=True,
                    timeout=0.05,
                )
                if pos_msg is not None:
                    self._pos_ned = np.array(
                        [pos_msg.x, pos_msg.y, pos_msg.z], dtype=np.float32
                    )
                    self._vel_ned = np.array(
                        [pos_msg.vx, pos_msg.vy, pos_msg.vz], dtype=np.float32
                    )

                # ATTITUDE — yaw + quaternion from ArduCopter EKF3
                att_msg = await asyncio.to_thread(
                    self._master.recv_match,
                    type="ATTITUDE",
                    blocking=True,
                    timeout=0.02,
                )
                if att_msg is not None:
                    self._yaw_rad      = att_msg.yaw
                    self._attitude_quat = self._euler_to_quat(
                        att_msg.roll, att_msg.pitch, att_msg.yaw
                    )

                # IMU from OAK-D BMI270 (6-axis: accel + gyro)
                self._poll_imu()

            except Exception as exc:
                logger.warning(f"[AVOID] Telemetry loop: {exc}")

            elapsed = time.monotonic() - t_start
            await asyncio.sleep(max(0.0, _TELEMETRY_PERIOD - elapsed))

    def _poll_imu(self) -> None:
        """Non-blocking pull of latest BMI270 packet from OAK-D."""
        try:
            queue = self._oak.getOutputQueue("imu_out", maxSize=5, blocking=False)
            pkt   = queue.tryGet()
            if pkt is None or not pkt.packets:
                return
            latest = pkt.packets[-1]
            acc    = latest.acceleroMeter
            gyro   = latest.gyroscope
            self._latest_imu = np.array(
                [acc.x, acc.y, acc.z, gyro.x, gyro.y, gyro.z], dtype=np.float32
            )
        except Exception as exc:
            logger.debug(f"[AVOID] IMU poll: {exc}")

    # ── Heartbeat loop (1 Hz) ─────────────────────────────────────────────────

    async def _heartbeat_loop(self) -> None:
        """Send MAV_TYPE_ONBOARD_CONTROLLER heartbeat — prevents ArduPilot GCS failsafe."""
        while self._running:
            try:
                await asyncio.to_thread(
                    self._master.mav.heartbeat_send,
                    _MAV_TYPE_ONBOARD_CONTROLLER,
                    _MAV_AUTOPILOT_INVALID,
                    0, 0, 0,
                )
            except Exception as exc:
                logger.warning(f"[AVOID] Heartbeat failed: {exc}")
            await asyncio.sleep(_HEARTBEAT_PERIOD)

    # ── Watchdog loop (2 Hz) ──────────────────────────────────────────────────

    async def _watchdog_loop(self) -> None:
        """Detect: stalled control loop, stale OAK-D frames."""
        while self._running:
            await asyncio.sleep(_WATCHDOG_PERIOD)
            now = time.monotonic()

            # Control loop liveness — must fire within _STALL_TIMEOUT_S
            if (
                self._goal_event is not None
                and self._goal_event.is_set()
                and self._last_control_time > 0
            ):
                stall = now - self._last_control_time
                if stall > _STALL_TIMEOUT_S:
                    logger.warning(
                        f"[AVOID] Control loop stalled ({stall:.2f} s) — holding position"
                    )
                    try:
                        await asyncio.to_thread(
                            self._publish_position,
                            self._pos_ned,
                            np.zeros(3, dtype=np.float32),
                        )
                    except Exception:
                        pass

            # OAK-D frame liveness
            if self._last_frame_time > 0:
                frame_age = now - self._last_frame_time
                if frame_age > _FRAME_TIMEOUT_S and self._avoidance_enabled:
                    logger.warning(
                        f"[AVOID] OAK-D frame stale ({frame_age:.2f} s) — disabling avoidance"
                    )
                    self._avoidance_enabled = False

    # ── MAVLink publish (single writer) ───────────────────────────────────────

    def _publish_position(
        self, target_ned: np.ndarray, vel_ff: np.ndarray
    ) -> None:
        """
        Send SET_POSITION_TARGET_LOCAL_NED.
        type_mask=0b0000110111000000: position + velocity active, rest ignored.
        This is the ONLY function that sends this message while avoidance is active.
        """
        self._master.mav.set_position_target_local_ned_send(
            0,                                  # time_boot_ms
            self._master.target_system,
            self._master.target_component,
            _MAV_FRAME_LOCAL_NED,
            _POS_VEL_TYPE_MASK,
            float(target_ned[0]),               # x (North)
            float(target_ned[1]),               # y (East)
            float(target_ned[2]),               # z (Down — negative = up)
            float(vel_ff[0]),                   # vx
            float(vel_ff[1]),                   # vy
            float(vel_ff[2]),                   # vz
            0.0, 0.0, 0.0,                      # ax, ay, az (ignored)
            0.0, 0.0,                           # yaw, yaw_rate (ignored)
        )

    # ── Coordinate helpers ────────────────────────────────────────────────────

    def _gps_to_ned(
        self, lat: float, lon: float, alt_msl: float
    ) -> np.ndarray:
        """
        Flat-earth GPS → NED conversion relative to EKF origin.
        Valid for distances < ~10 km. No altitude datum conversion needed
        (ArduCopter HOME_POSITION altitude is already MSL).
        """
        R_EARTH = 6_371_000.0
        dlat = math.radians(lat - self._origin_lat)
        dlon = math.radians(lon - self._origin_lon)
        north = dlat * R_EARTH
        east  = dlon * R_EARTH * math.cos(math.radians(self._origin_lat))
        down  = -(alt_msl - self._origin_alt)   # NED: down is positive
        return np.array([north, east, down], dtype=np.float32)

    @staticmethod
    def _body_to_ned(body_vec: np.ndarray, yaw_rad: float) -> np.ndarray:
        """
        Yaw-only body→NED rotation. Sufficient for near-level flight where
        roll/pitch corrections are small and the drone is near-horizontal.

        body_vec: [x_forward, y_right, z_down]
        Returns NED vector [north, east, down].
        """
        cos_y = math.cos(yaw_rad)
        sin_y = math.sin(yaw_rad)
        north = cos_y * body_vec[0] - sin_y * body_vec[1]
        east  = sin_y * body_vec[0] + cos_y * body_vec[1]
        down  = body_vec[2]
        return np.array([north, east, down], dtype=np.float32)

    def _decompose_path(
        self, start: np.ndarray, end: np.ndarray
    ) -> List[np.ndarray]:
        """
        Decompose path into sub-goals at AVOIDANCE_SUB_GOAL_SPACING_M spacing.
        The last sub-goal is always exactly `end` (ensures arrival detection works).
        """
        total_dist = float(np.linalg.norm(end - start))
        if total_dist <= AVOIDANCE_SUB_GOAL_SPACING_M:
            return [end.copy()]

        n_segs = math.ceil(total_dist / AVOIDANCE_SUB_GOAL_SPACING_M)
        ts = np.linspace(0.0, 1.0, n_segs + 1)[1:]  # exclude t=0 (start point)
        return [start + t * (end - start) for t in ts]

    def _apply_line_constrained_correction(
        self,
        sub_goal: np.ndarray,
        prev_sub_goal: np.ndarray,
        corr_ned: np.ndarray,
    ) -> np.ndarray:
        """
        Clamp NED correction to ±AVOIDANCE_MAX_LATERAL_M lateral and
        ±AVOIDANCE_MAX_VERTICAL_M vertical from the current path segment.

        This prevents the avoidance system from deviating so far that the drone
        loses progress toward the goal or violates geofence boundaries.
        """
        path_vec  = sub_goal - prev_sub_goal
        path_h    = path_vec[:2]
        path_dist = float(np.linalg.norm(path_h))

        # Vertical clamp
        vert = float(np.clip(
            corr_ned[2],
            -AVOIDANCE_MAX_VERTICAL_M,
            AVOIDANCE_MAX_VERTICAL_M,
        ))

        if path_dist < 0.01:
            # Degenerate / vertical segment — clamp vertical only
            return np.array([corr_ned[0], corr_ned[1], vert], dtype=np.float32)

        # Lateral clamp: decompose horizontal correction into along-path + lateral
        path_unit = path_h / path_dist
        corr_ne   = corr_ned[:2]
        along     = float(np.dot(corr_ne, path_unit))
        lateral   = corr_ne - along * path_unit
        lat_mag   = float(np.linalg.norm(lateral))

        if lat_mag > AVOIDANCE_MAX_LATERAL_M:
            lateral = lateral * (AVOIDANCE_MAX_LATERAL_M / lat_mag)

        ne = along * path_unit + lateral
        return np.array([ne[0], ne[1], vert], dtype=np.float32)

    @staticmethod
    def _euler_to_quat(roll: float, pitch: float, yaw: float) -> np.ndarray:
        """Convert Euler angles (radians) to quaternion [w, x, y, z]."""
        cr, sr = math.cos(roll  / 2), math.sin(roll  / 2)
        cp, sp = math.cos(pitch / 2), math.sin(pitch / 2)
        cy, sy = math.cos(yaw   / 2), math.sin(yaw   / 2)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        return np.array([w, x, y, z], dtype=np.float32)

    def stop(self) -> None:
        """Signal all background tasks to exit on their next iteration."""
        self._running = False
        if self._goal_event is not None:
            self._goal_event.clear()
        logger.info("[AVOID] Controller stopped")
