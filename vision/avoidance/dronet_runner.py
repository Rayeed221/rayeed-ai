"""
DroNetRunner — autonomous avoidance background task (Layer 2).

Runs PULP-DroNet v3 on the OAK-D Lite at ~20 Hz as an asyncio coroutine.
Publishes AvoidanceState (thread-safe) and sends MAVLink velocity commands
directly when collision_prob exceeds COLL_THRESH.

This module never goes through the LLM or tool pipeline.
See AVOIDANCE_INTEGRATION_PLAN.txt for the two-layer architecture.
"""

import asyncio
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

try:
    from pymavlink import mavutil
    _MAVLINK_OK = True
except ImportError:
    _MAVLINK_OK = False


@dataclass
class AvoidanceState:
    collision_prob:  float   # 0.0 – 1.0
    steering:        float   # yaw-rate hint from CNN  [-1, +1]
    depth_mm:        float   # median center stereo depth (mm)
    horizontal_bias: float   # left/right depth asymmetry [-1, +1]
    vertical_bias:   float   # up/down depth asymmetry   [-1, +1]
    timestamp:       float   # time.monotonic()


class DroNetRunner:
    """
    Wraps the run_dronet_oak pipeline + MavlinkBridge into a single asyncio task.

    get_state() is thread-safe and may be called from any context.
    run()       is a coroutine; add it to the background task group in app.py.
    """

    COLL_THRESH        = 0.3    # velocity commands stop above this
    FORWARD_SPEED      = 0.5    # m/s cruise when no collision
    MAX_YAW_RATE_RAD   = 0.8    # rad/s at full steer deflection
    MAX_LATERAL_SPEED  = 0.3    # m/s at full lateral bias
    MAX_VERTICAL_SPEED = 0.2    # m/s at full vertical bias
    HB_INTERVAL        = 1.0    # MAVLink GCS heartbeat period (s)

    # type_mask: ignore pos(0-2), use vel(3-5), ignore accel(6-8),
    #            ignore yaw(9), use yaw_rate(10)
    _TYPE_MASK = (
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE
    ) if _MAVLINK_OK else 0x3C7

    def __init__(self, mav_connection_string: str, model_path: str):
        self._uri     = mav_connection_string
        self._blob    = Path(model_path)
        self._conn    = None
        self._last_hb = 0.0
        self._state: Optional[AvoidanceState] = None
        self._lock    = threading.Lock()

    # ── Public API ────────────────────────────────────────────────────────────

    def get_state(self) -> Optional[AvoidanceState]:
        with self._lock:
            return self._state

    async def run(self) -> None:
        """20 Hz inference + velocity command loop. Non-fatal on any setup failure."""
        try:
            import depthai  # noqa: F401
        except ImportError:
            logger.warning("[AVOIDANCE] depthai not installed — avoidance loop disabled")
            return

        if not self._blob.exists():
            logger.warning(f"[AVOIDANCE] Blob not found: {self._blob} — avoidance loop disabled")
            return

        await asyncio.to_thread(self._connect_mavlink)

        try:
            from vision.avoidance.run_dronet_oak import (
                build_pipeline,
                get_center_depth_mm,
                get_horizontal_bias,
                get_vertical_bias,
                DEPTH_COLLISION_MM,
            )
        except Exception as exc:
            logger.warning(f"[AVOIDANCE] Cannot import pipeline helpers: {exc}")
            return

        logger.info(f"[AVOIDANCE] DroNet loop starting — blob={self._blob}")

        def _init_pipeline():
            p, q_nn, _q_prev, q_depth = build_pipeline(self._blob, True)
            p.start()
            return p, q_nn, q_depth

        try:
            pipeline, q_nn, q_depth = await asyncio.to_thread(_init_pipeline)
        except Exception as exc:
            logger.warning(f"[AVOIDANCE] Pipeline start failed: {exc}")
            return

        depth_mm = 0.0
        lateral  = 0.0
        vertical = 0.0

        try:
            while pipeline.isRunning():
                if q_depth is not None:
                    depth_data = q_depth.tryGet()
                    if depth_data is not None:
                        df       = depth_data.getCvFrame()
                        depth_mm = get_center_depth_mm(df)
                        lateral  = get_horizontal_bias(df)
                        vertical = get_vertical_bias(df)

                nn_data = q_nn.tryGet()
                if nn_data is not None:
                    try:
                        steer_raw = float(nn_data.getTensor("steer").flat[0])
                        coll_raw  = float(nn_data.getTensor("coll").flat[0])
                    except Exception:
                        t         = nn_data.getFirstTensor()
                        steer_raw = float(t.flat[0])
                        coll_raw  = float(t.flat[1])

                    steer    = float(np.clip(steer_raw, -1.0, 1.0))
                    coll_raw = float(np.clip(coll_raw,  0.0, 1.0))
                    coll     = 1.0 if (depth_mm > 0 and depth_mm < DEPTH_COLLISION_MM) else coll_raw

                    state = AvoidanceState(
                        collision_prob  = coll,
                        steering        = steer,
                        depth_mm        = depth_mm,
                        horizontal_bias = lateral,
                        vertical_bias   = vertical,
                        timestamp       = time.monotonic(),
                    )
                    with self._lock:
                        self._state = state

                    if coll >= self.COLL_THRESH:
                        await asyncio.to_thread(
                            self._send_velocity, steer, coll, lateral, vertical
                        )

                await asyncio.sleep(0.05)   # ~20 Hz

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.exception(f"[AVOIDANCE] Runtime error: {exc}")
        finally:
            try:
                pipeline.stop()
            except Exception:
                pass
            if self._conn is not None:
                try:
                    self._conn.close()
                except Exception:
                    pass
            logger.info("[AVOIDANCE] DroNet loop stopped")

    # ── MAVLink helpers ───────────────────────────────────────────────────────

    def _connect_mavlink(self) -> None:
        if not _MAVLINK_OK:
            return
        try:
            self._conn = mavutil.mavlink_connection(
                self._uri, source_system=254, source_component=0
            )
            if self._conn.wait_heartbeat(timeout=5) is None:
                logger.warning("[AVOIDANCE] No MAVLink heartbeat — velocity commands disabled")
                self._conn = None
            else:
                logger.info(f"[AVOIDANCE] MAVLink connected: {self._uri}")
        except Exception as exc:
            logger.warning(f"[AVOIDANCE] MAVLink connect failed ({exc}) — velocity commands disabled")
            self._conn = None

    def _send_velocity(self, steer: float, coll: float,
                       lateral: float, vertical: float) -> None:
        if self._conn is None:
            return
        now = time.time()

        if now - self._last_hb >= self.HB_INTERVAL:
            try:
                self._conn.mav.heartbeat_send(
                    mavutil.mavlink.MAV_TYPE_GCS,
                    mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                    0, 0, 0,
                )
            except Exception:
                pass
            self._last_hb = now

        if coll > self.COLL_THRESH:
            vx = vy = vz = yaw_rate = 0.0
        else:
            vx       = self.FORWARD_SPEED
            vy       = float(np.clip(lateral,  -1.0, 1.0)) * self.MAX_LATERAL_SPEED
            vz       = float(np.clip(vertical, -1.0, 1.0)) * self.MAX_VERTICAL_SPEED
            yaw_rate = float(np.clip(steer,    -1.0, 1.0)) * self.MAX_YAW_RATE_RAD

        try:
            self._conn.mav.set_position_target_local_ned_send(
                int((now % 1e6) * 1000),
                self._conn.target_system,
                self._conn.target_component,
                mavutil.mavlink.MAV_FRAME_BODY_NED,
                self._TYPE_MASK,
                0, 0, 0,
                vx, vy, vz,
                0, 0, 0,
                0.0,
                yaw_rate,
            )
        except Exception as exc:
            logger.debug(f"[AVOIDANCE] MAVLink send error: {exc}")
