"""
Run tiny-PULP-DroNet v3 on the OAK-D Lite camera using depthai v3.

Usage:
    python run_dronet_oak.py [--blob PATH] [--no-depth]

Prerequisites:
    1. pip install -r requirements.txt
    2. python export_to_onnx.py           # creates dronet_tiny.onnx
    3. python convert_to_blob.py          # creates dronet_tiny.blob
    4. Connect OAK-D Lite via USB

Pipeline (DepthAI v3 — queues created directly on node outputs via
node.output.createOutputQueue(), no XLinkOut nodes):
    LEFT mono camera (CAM_B, native grayscale)
        ├─► ImageManip  (crop 245,72→1035,728 then resize 200×200)
        │       ├─► NeuralNetwork (dronet_tiny.blob)
        │       │       └─► nn.out.createOutputQueue()    → steer + coll from CNN
        │       └─► manip.out.createOutputQueue()         → 200×200 frame for display
        └─► StereoDepth (with RIGHT camera)
                └─► stereo.depth.createOutputQueue()      → depth map for safety override

== Why LEFT mono camera instead of RGB ==
The model was trained on images from the Himax HM01B0 — a monochrome
QVGA camera on the CrazyFlie AI-deck. The OAK-D Lite's LEFT/RIGHT stereo
cameras (OV9282) are already monochrome, which is a much closer match to
the training sensor than converting the RGB camera to grayscale.

== Why this specific crop ==
Training used transforms.CenterCrop(200) on 324×244 Himax images, which
keeps the centre 61.73% of horizontal and 81.97% of vertical pixels.
Applying those same fractions to the mono camera's native 1280×800 gives
a 790×656 centre crop, which we then resize to 200×200. This is the
closest achievable match to the training preprocessing geometry.

    Himax 324×244 → CenterCrop(200):  x0=62, y0=22 → x1=262, y1=222
    Mono  1280×800 → equiv crop:       x0=245, y0=72 → x1=1035, y1=728
                                       (790×656) → resize → 200×200

== Depth safety override ==
The collision labels in training were set to 1 when an obstacle was
within 2 m (measured by the VL53L1x ToF sensor). The OAK-D Lite's stereo
depth provides the same kind of frontal distance measurement. If the
median depth in the central ROI of the depth map is < 2000 mm, we force
collision = 1.0, regardless of what the CNN outputs. This is a hard
safety guarantee on top of the learned model.

Model outputs:
    steer : yaw-rate in [-1, +1]  (positive = go right, negative = go left)
    coll  : collision probability in [0, 1]
"""

import argparse
import time
from pathlib import Path

import cv2
import numpy as np

try:
    from pymavlink import mavutil
    _MAVLINK_AVAILABLE = True
except ImportError:
    _MAVLINK_AVAILABLE = False

SCRIPT_DIR   = Path(__file__).resolve().parent
# DEFAULT_BLOB = SCRIPT_DIR / "dronet_tiny.blob"
DEFAULT_BLOB = SCRIPT_DIR / "dronet_tiny_openvino_2022.1_5shave.blob"

# ---------------------------------------------------------------------------
# Preprocessing constants (match training CenterCrop(200) from 324×244 Himax)
# ---------------------------------------------------------------------------
# OAK-D Lite OV9282 mono cameras only support GRAY8 output in binned 640×400
# mode (not 1280×800). We use 640×400 and halve the crop coordinates:
#   Fraction from Himax 324×244:  horiz=200/324=0.6173, vert=200/244=0.8197
#   Applied to 1280×800: x0=245,y0=72, x1=1035,y1=728 → 790×656
#   Halved for 640×400:  x0=122,y0=36, x1=517,y1=364  → 395×328 → 200×200
MONO_W, MONO_H       = 640, 400
CROP_X0, CROP_Y0     = 122, 36
CROP_X1, CROP_Y1     = 517, 364   # 395×328 crop → resize → 200×200
MODEL_INPUT_SIZE     = 200

# Collision threshold matching training label definition (2 m = 2000 mm)
DEPTH_COLLISION_MM   = 2000
# Central ROI of the depth map used for obstacle distance (fraction of w/h)
DEPTH_ROI_FRAC       = 0.15

# ---------------------------------------------------------------------------
# Display constants
# ---------------------------------------------------------------------------
DISP_SCALE = 3
DISP_W     = MODEL_INPUT_SIZE * DISP_SCALE          # 600
DISP_H     = MODEL_INPUT_SIZE * DISP_SCALE + 130    # 730

# BGR colours
WHITE  = (255, 255, 255)
GREEN  = (0,   200, 0)
RED    = (0,   0,   220)
YELLOW = (0,   200, 200)
BLUE   = (220, 100, 0)
ORANGE = (0,   140, 255)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def draw_overlay(
    canvas: np.ndarray,
    steer: float,
    lateral: float,
    vertical: float,
    coll: float,
    coll_raw: float,
    depth_mm: float,
    fps: float,
    depth_override: bool,
):
    h, w    = canvas.shape[:2]
    img_h   = MODEL_INPUT_SIZE * DISP_SCALE
    gauge_y = img_h

    cv2.rectangle(canvas, (0, gauge_y), (w, h), (30, 30, 30), -1)

    # -----------------------------------------------------------------------
    # 2D avoidance arrow drawn on the camera image
    # steer   : yaw from model  (+1 = go right,  -1 = go left)
    # lateral : depth left/right asymmetry  (+1 = go right, -1 = go left)
    # vertical: depth top/bottom asymmetry  (+1 = go down,  -1 = go up)
    # Arrow tip shows the combined avoidance direction from drone's perspective.
    # In OpenCV image coordinates: +x = right, +y = down.
    # vertical > 0 means go down in the real world → arrow tip moves DOWN (+y).
    # -----------------------------------------------------------------------
    cx  = w // 2
    cy  = img_h // 2

    ARROW_SCALE = 100
    dx_raw = (steer + lateral) * 0.5   # average two horizontal sources → [-1, +1]
    dy_raw = vertical                   # depth vertical bias → [-1, +1]
    dx = int(dx_raw * ARROW_SCALE)
    dy = int(dy_raw * ARROW_SCALE)     # +dy = down on screen = go down in world

    magnitude = int((dx**2 + dy**2) ** 0.5)
    arrow_col = YELLOW if magnitude < 15 else (RED if coll > 0.5 else GREEN)

    if magnitude > 5:
        cv2.arrowedLine(canvas, (cx, cy), (cx + dx, cy + dy),
                        arrow_col, 4, tipLength=0.35)
    else:
        cv2.circle(canvas, (cx, cy), 10, YELLOW, 2)

    # Crosshair at centre
    cv2.line(canvas, (cx - 15, cy), (cx + 15, cy), (80, 80, 80), 1)
    cv2.line(canvas, (cx, cy - 15), (cx, cy + 15), (80, 80, 80), 1)

    # -----------------------------------------------------------------------
    # Direction label (bottom of image, above gauge)
    # -----------------------------------------------------------------------
    if abs(dx_raw) < 0.15 and abs(dy_raw) < 0.15:
        dir_txt = "STRAIGHT"
    elif abs(dy_raw) > abs(dx_raw):
        dir_txt = "DOWN" if dy_raw > 0 else "UP"
    else:
        dir_txt = "RIGHT" if dx_raw > 0 else "LEFT"
    dir_col = YELLOW if dir_txt == "STRAIGHT" else arrow_col
    cv2.putText(canvas, dir_txt, (w - 140, img_h - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, dir_col, 2)

    # -----------------------------------------------------------------------
    # Gauge panel
    # -----------------------------------------------------------------------
    cv2.putText(canvas,
                f"Steer: {steer:+.3f}  Lat: {lateral:+.3f}  Vert: {vertical:+.3f}",
                (10, gauge_y + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.48, WHITE, 1)

    # --- Collision bar ---
    bar_x0, bar_y0 = 10, gauge_y + 42
    bar_w,  bar_h  = w - 20, 20
    filled  = int(bar_w * float(np.clip(coll, 0, 1)))
    bar_col = RED if coll > 0.5 else GREEN
    cv2.rectangle(canvas, (bar_x0, bar_y0),
                  (bar_x0 + bar_w, bar_y0 + bar_h), (70, 70, 70), -1)
    cv2.rectangle(canvas, (bar_x0, bar_y0),
                  (bar_x0 + filled, bar_y0 + bar_h), bar_col, -1)
    cv2.rectangle(canvas, (bar_x0, bar_y0),
                  (bar_x0 + bar_w, bar_y0 + bar_h), WHITE, 1)

    coll_label = f"Collision: {coll:.3f}"
    if depth_override:
        coll_label += f"  [depth override: {depth_mm/1000:.2f}m]"
    elif coll > 0.5:
        coll_label += "  !!!"
    cv2.putText(canvas, coll_label, (bar_x0, bar_y0 - 3),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, bar_col, 1)

    # --- Depth readout ---
    depth_str = f"Depth: {depth_mm/1000:.2f} m" if depth_mm > 0 else "Depth: --"
    depth_col = RED if 0 < depth_mm < DEPTH_COLLISION_MM else WHITE
    cv2.putText(canvas, depth_str, (10, gauge_y + 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, depth_col, 1)

    # --- CNN raw (before override) ---
    if depth_override:
        cv2.putText(canvas, f"CNN raw: {coll_raw:.3f}",
                    (10, gauge_y + 112),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, ORANGE, 1)

    # --- FPS ---
    cv2.putText(canvas, f"FPS: {fps:.1f}", (w - 100, gauge_y + 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, WHITE, 1)

    # --- Obstacle banner ---
    if depth_override:
        cv2.rectangle(canvas, (0, 0), (w, 26), RED, -1)
        cv2.putText(canvas, "! OBSTACLE DETECTED (depth < 2 m) !",
                    (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, WHITE, 2)


# ---------------------------------------------------------------------------
# MAVLink bridge
# ---------------------------------------------------------------------------

class MavlinkBridge:
    """
    Sends DroNet outputs to a flight controller via MAVLink TCP.

    DroNet was designed for a vehicle that moves forward continuously while
    yawing to steer. To replicate this on a multirotor we send
    SET_POSITION_TARGET_LOCAL_NED (msg #84) in MAV_FRAME_BODY_NED so the
    drone moves forward at a fixed speed while yaw rate is set from steer.

    type_mask = 0x03C7  → use vx, vy, vz and yaw_rate; ignore everything else
      vx        = FORWARD_SPEED (m/s) — constant cruise, zeroed on collision
      vy        = 0   (no lateral/strafe — model not trained for it)
      vz        = 0   (altitude hold)
      yaw_rate  = steer × MAX_YAW_RATE_RAD  (rad/s)

    On collision (coll > COLL_THRESH): all velocities and yaw rate set to 0.

    Requires the FC to be in GUIDED mode before commands take effect.
    Default URL: tcp:127.0.0.1:5760  (ArduPilot SITL default)
                 tcp:127.0.0.1:5762  (MAVProxy secondary output)
    """

    HB_INTERVAL       = 1.0   # heartbeat period (s)
    COLL_THRESH       = 0.3
    FORWARD_SPEED     = 0.5   # m/s cruise speed when no collision (body x = forward)
    MAX_YAW_RATE_RAD  = 0.8   # rad/s at full steer deflection (~45 °/s)
    MAX_LATERAL_SPEED = 0.3   # m/s at full lateral bias (body y = right)
    MAX_VERTICAL_SPEED = 0.2  # m/s at full vertical bias (body/NED z = down)

    # type_mask: ignore pos(0-2), use vel(3-5), ignore accel(6-8),
    #            ignore yaw(9), use yaw_rate(10)  →  bits 0,1,2,6,7,8,9 = 0x1C7 | 0x200 = 0x3C7
    _TYPE_MASK = (
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE
        | mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE
    ) if _MAVLINK_AVAILABLE else 0x3C7

    def __init__(self, url: str = "tcp:127.0.0.1:5763"):
        self._url     = url
        self._conn    = None
        self._last_hb = 0.0

    def connect(self) -> bool:
        if not _MAVLINK_AVAILABLE:
            print("WARNING: pymavlink not installed — MAVLink disabled. "
                  "Run: pip install pymavlink")
            return False
        try:
            print(f"MAVLink     : connecting to {self._url} ...")
            self._conn = mavutil.mavlink_connection(
                self._url,
                source_system=255,
                source_component=0,
            )
            hb = self._conn.wait_heartbeat(timeout=5)
            if hb is None:
                print("MAVLink     : no heartbeat received — continuing without FC")
                self._conn = None
                return False
            print(f"MAVLink     : heartbeat from system {self._conn.target_system} "
                  f"component {self._conn.target_component}")
            print("MAVLink     : set FC to GUIDED mode before arming")
            return True
        except Exception as exc:
            print(f"MAVLink     : connection failed ({exc}) — inference will still run")
            self._conn = None
            return False

    def send(self, steer: float, coll: float,
             lateral: float = 0.0, vertical: float = 0.0) -> None:
        """
        Send SET_POSITION_TARGET_LOCAL_NED in MAV_FRAME_BODY_NED.

        Body-frame mapping from model/depth outputs (drone perspective):
          vx        = FORWARD_SPEED (constant cruise; 0 on collision)
          vy        = lateral * MAX_LATERAL_SPEED
                      lateral > 0 → obstacle left  → avoid right → vy > 0 (body right)
          vz        = vertical * MAX_VERTICAL_SPEED
                      vertical > 0 → obstacle above → avoid down  → vz > 0 (NED down)
          yaw_rate  = steer * MAX_YAW_RATE_RAD
                      steer > 0 → go right → positive yaw (clockwise in NED)
        All outputs zeroed when coll > COLL_THRESH.
        """
        if self._conn is None:
            return

        now = time.time()

        # Periodic heartbeat — FC drops GCS link if it stops receiving these
        if now - self._last_hb >= self.HB_INTERVAL:
            self._conn.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,
                mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                0, 0, 0,
            )
            self._last_hb = now

        if coll > self.COLL_THRESH:
            vx = vy = vz = yaw_rate = 0.0
        else:
            vx       = self.FORWARD_SPEED
            vy       = float(np.clip(lateral,  -1.0, 1.0)) * self.MAX_LATERAL_SPEED
            vz       = float(np.clip(vertical, -1.0, 1.0)) * self.MAX_VERTICAL_SPEED
            yaw_rate = float(np.clip(steer,    -1.0, 1.0)) * self.MAX_YAW_RATE_RAD

        self._conn.mav.set_position_target_local_ned_send(
            int((now % 1e6) * 1000),             # time_boot_ms (wrapping is fine)
            self._conn.target_system,
            self._conn.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_NED,  # body frame: x=fwd, y=right, z=down
            self._TYPE_MASK,
            0, 0, 0,        # x, y, z position (ignored)
            vx, vy, vz,     # vx (forward), vy (right strafe), vz (down)
            0, 0, 0,        # ax, ay, az (ignored)
            0.0,            # yaw angle (ignored)
            yaw_rate,       # yaw_rate (rad/s, positive = clockwise = nose right)
        )

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None


# ---------------------------------------------------------------------------
# Pipeline builder
# ---------------------------------------------------------------------------

def build_pipeline(blob_path: Path, use_depth: bool = True):
    """
    Build depthai v3 Pipeline and return (pipeline, q_nn, q_prev, q_depth).

    LEFT mono camera (CAM_B) → ImageManip crop+resize 200×200 → NeuralNetwork
    LEFT + RIGHT mono (CAM_C) → StereoDepth             (if use_depth=True)

    Uses v3 API: Camera.build(socket), createOutputQueue(), with pipeline context.
    """
    import depthai as dai

    pipeline = dai.Pipeline()

    # ------------------------------------------------------------------
    # LEFT mono camera  (CAM_B = OV9282, native grayscale)
    # ------------------------------------------------------------------
    left_cam = pipeline.create(dai.node.Camera).build(
        dai.CameraBoardSocket.CAM_B
    )
    left_out = left_cam.requestOutput(
        (MONO_W, MONO_H), type=dai.ImgFrame.Type.GRAY8
    )

    # ------------------------------------------------------------------
    # ImageManip: centre-crop 790×656 then resize to 200×200
    # v3 API: addCrop(x, y, w, h) + setOutputSize(w, h)
    # ------------------------------------------------------------------
    CROP_W = CROP_X1 - CROP_X0   # 790
    CROP_H = CROP_Y1 - CROP_Y0   # 656
    manip = pipeline.create(dai.node.ImageManip)
    manip.initialConfig.addCrop(CROP_X0, CROP_Y0, CROP_W, CROP_H)
    manip.initialConfig.setOutputSize(MODEL_INPUT_SIZE, MODEL_INPUT_SIZE)
    manip.initialConfig.setFrameType(dai.ImgFrame.Type.GRAY8)
    manip.setMaxOutputFrameSize(MODEL_INPUT_SIZE * MODEL_INPUT_SIZE)
    left_out.link(manip.inputImage)

    # ------------------------------------------------------------------
    # NeuralNetwork: DroNet on MyriadX VPU
    # blob input: (1,1,200,200) — scale_values=255 applied by VPU
    # ------------------------------------------------------------------
    nn = pipeline.create(dai.node.NeuralNetwork)
    nn.setBlobPath(blob_path)
    nn.setNumInferenceThreads(2)
    nn.input.setBlocking(False)
    nn.input.setMaxSize(1)
    manip.out.link(nn.input)

    # ------------------------------------------------------------------
    # StereoDepth: CAM_B (left) + CAM_C (right)
    # ------------------------------------------------------------------
    q_depth = None
    if use_depth:
        right_cam = pipeline.create(dai.node.Camera).build(
            dai.CameraBoardSocket.CAM_C
        )
        right_out = right_cam.requestOutput(
            (MONO_W, MONO_H), type=dai.ImgFrame.Type.GRAY8
        )

        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.setDefaultProfilePreset(
            dai.node.StereoDepth.PresetMode.DENSITY
        )
        stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)
        stereo.setOutputSize(MONO_W, MONO_H)

        left_out.link(stereo.left)
        right_out.link(stereo.right)

        q_depth = stereo.depth.createOutputQueue(maxSize=4, blocking=False)

    # ------------------------------------------------------------------
    # Output queues (v3: createOutputQueue replaces XLinkOut)
    # ------------------------------------------------------------------
    q_nn   = nn.out.createOutputQueue(maxSize=4, blocking=False)
    q_prev = manip.out.createOutputQueue(maxSize=4, blocking=False)

    return pipeline, q_nn, q_prev, q_depth


def get_center_depth_mm(depth_frame: np.ndarray) -> float:
    """
    Return the median non-zero depth (mm) inside a central ROI of the
    depth map. Returns 0.0 if no valid measurements exist.
    """
    h, w = depth_frame.shape
    roi_h = int(h * DEPTH_ROI_FRAC)
    roi_w = int(w * DEPTH_ROI_FRAC)
    y0 = (h - roi_h) // 2
    x0 = (w - roi_w) // 2
    roi = depth_frame[y0:y0 + roi_h, x0:x0 + roi_w]
    valid = roi[roi > 0]
    return float(np.median(valid)) if valid.size > 0 else 0.0


def get_horizontal_bias(depth_frame: np.ndarray) -> float:
    """
    Estimate horizontal avoidance direction from stereo depth.

    Splits the central ROI into left and right halves and compares their
    median depths. Returns a value in [-1, +1]:
      +1 = right half much closer → obstacle right → go LEFT
      -1 = left half much closer  → obstacle left  → go RIGHT
       0 = symmetric / no clear horizontal threat

    Sign convention matches steer: positive = go right (avoid left obstacle).
    """
    h, w = depth_frame.shape
    roi_h = int(h * DEPTH_ROI_FRAC)
    roi_w = int(w * DEPTH_ROI_FRAC)
    y0 = (h - roi_h) // 2
    x0 = (w - roi_w) // 2
    roi = depth_frame[y0:y0 + roi_h, x0:x0 + roi_w]

    mid = roi_w // 2
    left_valid  = roi[:, :mid][roi[:, :mid] > 0]
    right_valid = roi[:, mid:][roi[:, mid:] > 0]

    if left_valid.size == 0 or right_valid.size == 0:
        return 0.0

    left_med  = float(np.median(left_valid))
    right_med = float(np.median(right_valid))

    total = left_med + right_med
    if total < 1.0:
        return 0.0
    # positive = left closer = go right (matches steer sign convention)
    bias = (right_med - left_med) / total   # [-1, +1]

    if abs(bias) < 0.05:
        return 0.0
    return float(np.clip(bias, -1.0, 1.0))


def get_vertical_bias(depth_frame: np.ndarray) -> float:
    """
    Estimate vertical avoidance direction from stereo depth.

    Splits the central ROI into top and bottom halves and compares their
    median depths. Returns a value in [-1, +1]:
      +1 = top half much closer  → obstacle above → go DOWN
      -1 = bottom half much closer → obstacle below → go UP
       0 = symmetric / no clear vertical threat

    Only returns a non-zero value when depth is valid and the asymmetry
    exceeds a minimum threshold (avoids noise-driven corrections).
    """
    h, w = depth_frame.shape
    roi_h = int(h * DEPTH_ROI_FRAC)
    roi_w = int(w * DEPTH_ROI_FRAC)
    y0 = (h - roi_h) // 2
    x0 = (w - roi_w) // 2
    roi = depth_frame[y0:y0 + roi_h, x0:x0 + roi_w]

    mid = roi_h // 2
    top_valid    = roi[:mid, :][roi[:mid, :] > 0]
    bottom_valid = roi[mid:, :][roi[mid:, :] > 0]

    if top_valid.size == 0 or bottom_valid.size == 0:
        return 0.0

    top_med    = float(np.median(top_valid))
    bottom_med = float(np.median(bottom_valid))

    # Normalise asymmetry: positive = top closer = go down
    total = top_med + bottom_med
    if total < 1.0:
        return 0.0
    bias = (bottom_med - top_med) / total   # [-1, +1]

    # Suppress small noise (< 5 % asymmetry)
    if abs(bias) < 0.08:
        return 0.0
    return float(np.clip(bias, -1.0, 1.0))


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def run(blob_path: Path, use_depth: bool = True, mav: "MavlinkBridge | None" = None):
    import depthai as dai

    if not blob_path.exists():
        print(f"ERROR: blob not found at {blob_path}")
        print("Run the following steps first:")
        print("  python export_to_onnx.py")
        print("  python convert_to_blob.py")
        return

    print(f"Blob        : {blob_path}")
    print(f"Depth layer : {'enabled' if use_depth else 'disabled'}")
    print(f"MAVLink     : {'enabled' if mav else 'disabled'}")
    print("Building pipeline...")
    pipeline, q_nn, q_prev, q_depth = build_pipeline(blob_path, use_depth=use_depth)

    print("Connecting to OAK-D Lite...")
    pipeline.start()
    print("Connected. Press 'q' or ESC to quit.\n")

    try:
        fps_counter  = 0
        fps_t0       = time.time()
        fps          = 0.0
        depth_mm     = 0.0
        lateral      = 0.0   # horizontal avoidance bias (+1 = go right)
        vertical     = 0.0   # vertical avoidance bias  (+1 = go down)
        canvas       = np.zeros((DISP_H, DISP_W, 3), dtype=np.uint8)

        while pipeline.isRunning():
            nn_data    = q_nn.tryGet()
            frame      = q_prev.tryGet()
            depth_data = q_depth.tryGet() if q_depth else None

            # ---- Update depth measurements ----
            if depth_data is not None:
                depth_frame = depth_data.getCvFrame()   # uint16 mm
                depth_mm    = get_center_depth_mm(depth_frame)
                lateral     = get_horizontal_bias(depth_frame)
                vertical    = get_vertical_bias(depth_frame)

            # ---- Update camera display ----
            if frame is not None:
                gray = frame.getCvFrame()               # (200, 200) uint8
                bgr  = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                upsc = cv2.resize(
                    bgr,
                    (DISP_W, MODEL_INPUT_SIZE * DISP_SCALE),
                    interpolation=cv2.INTER_NEAREST,
                )
                canvas[: MODEL_INPUT_SIZE * DISP_SCALE, :] = upsc

            # ---- Process NN output ----
            if nn_data is not None:
                # print(nn_data)
                
                try:
                    steer_raw = float(nn_data.getTensor("steer").flat[0])
                    coll_raw  = float(nn_data.getTensor("coll").flat[0])
                except Exception:
                    t         = nn_data.getFirstTensor()
                    steer_raw = float(t.flat[0])
                    coll_raw  = float(t.flat[1])

                steer    = float(np.clip(steer_raw, -1.0, 1.0))
                coll_raw = float(np.clip(coll_raw,  0.0, 1.0))

                # Depth safety override: obstacle within 2 m → force coll=1
                depth_override = (
                    use_depth
                    and depth_mm > 0
                    and depth_mm < DEPTH_COLLISION_MM
                )
                coll = 1.0 if depth_override else coll_raw

                fps_counter += 1
                elapsed = time.time() - fps_t0
                if elapsed >= 1.0:
                    fps          = fps_counter / elapsed
                    fps_counter  = 0
                    fps_t0       = time.time()

                if mav:
                    mav.send(steer, coll, lateral=lateral, vertical=vertical)

                draw_overlay(
                    canvas, steer, lateral, vertical, coll, coll_raw, depth_mm, fps, depth_override
                )
                mav_tag = "  [MAV TX]" if mav else ""
                print(
                    f"\rsteer={steer:+.4f}  lateral={lateral:+.4f}"
                    f"  coll={coll:.4f}  depth={depth_mm/1000:.2f}m  fps={fps:.1f}{mav_tag}   ",
                    end="",
                    flush=True,
                )

            cv2.imshow("PULP-DroNet v3 — OAK-D Lite", canvas)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                print()
                break

    finally:
        pipeline.stop()
        if mav:
            mav.close()
    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Run PULP-DroNet v3 on OAK-D Lite via depthai v3"
    )
    parser.add_argument(
        "--blob",
        type=Path,
        default=DEFAULT_BLOB,
        help=f"Path to MyriadX blob (default: {DEFAULT_BLOB})",
    )
    parser.add_argument(
        "--no-depth",
        action="store_true",
        help="Disable stereo depth safety layer (CNN-only mode)",
    )
    parser.add_argument(
        "--mavlink",
        action="store_true",
        help="Enable MAVLink output (requires pymavlink)",
    )
    parser.add_argument(
        "--mavlink-url",
        default="tcp:127.0.0.1:5763",
        help="MAVLink connection URL (default: tcp:127.0.0.1:5763)",
    )
    parser.add_argument(
        "--forward-speed",
        type=float,
        default=MavlinkBridge.FORWARD_SPEED,
        help="Cruise forward speed in m/s when no collision (default: "
             f"{MavlinkBridge.FORWARD_SPEED})",
    )
    parser.add_argument(
        "--max-yaw-rate",
        type=float,
        default=MavlinkBridge.MAX_YAW_RATE_RAD,
        help="Yaw rate at full steer deflection in rad/s (default: "
             f"{MavlinkBridge.MAX_YAW_RATE_RAD})",
    )
    args = parser.parse_args()

    mav = None
    if args.mavlink:
        mav = MavlinkBridge(url=args.mavlink_url)
        mav.FORWARD_SPEED    = args.forward_speed
        mav.MAX_YAW_RATE_RAD = args.max_yaw_rate
        mav.connect()   # non-fatal — inference runs even if FC unreachable

    run(args.blob, use_depth=not args.no_depth, mav=mav)


if __name__ == "__main__":
    main()
