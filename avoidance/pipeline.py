"""
DepthAI pipeline builder for OAK-D Lite obstacle avoidance.

Hardware notes:
  - OAK-D Lite cameras: OV7251 monochrome, 640×480 @ 10 fps (CAM_B=left, CAM_C=right)
  - StereoDepth: hardware SGM — no SHAVEs consumed, dedicated pipeline
  - NeuralNetwork: encoder .blob on MyriadX VPU (6 SHAVEs, FP16)
  - IMU: BMI270 6-axis ONLY (accel + gyro) — NO magnetometer, NO rotation vector
    Attitude must come from ArduCopter ATTITUDE message (EKF3 fusion), not IMU alone.

SHAVE budget: Camera ISP ~3, ImageManip ~1, CNN blob 6 → ~10 of 16 SHAVEs.

OpenVINO constraint: encoder blob MUST be compiled with OpenVINO ≤2022.3.
                     OpenVINO 2023+ dropped MyriadX (MYRIAD plugin removed).

GRU does NOT run on-device — it runs on RPi5 via ONNX Runtime (see avoidance_controller.py).
"""

from typing import Tuple


def build_avoidance_pipeline(blob_path: str) -> Tuple:
    """
    Build and return the DepthAI pipeline for stereo depth + CNN encoder + IMU.

    Args:
        blob_path: path to compiled MyriadX encoder blob (depth_encoder_6shaves.blob)

    Returns:
        (pipeline, nn_queue_name, imu_queue_name)
          pipeline:       dai.Pipeline instance (pass to dai.Device())
          nn_queue_name:  "nn_out" — XLinkOut stream for encoder feature vectors [64]
          imu_queue_name: "imu_out" — XLinkOut stream for IMU packets (accel+gyro)
    """
    import depthai as dai

    pipeline = dai.Pipeline()

    # ── Mono cameras (OV7251, 400P) ───────────────────────────────────────────
    cam_left  = pipeline.create(dai.node.MonoCamera)
    cam_right = pipeline.create(dai.node.MonoCamera)

    cam_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    cam_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    cam_left.setBoardSocket(dai.CameraBoardSocket.CAM_B)
    cam_right.setBoardSocket(dai.CameraBoardSocket.CAM_C)
    cam_left.setFps(10)
    cam_right.setFps(10)

    # ── StereoDepth (hardware SGM — no SHAVE cost) ────────────────────────────
    stereo = pipeline.create(dai.node.StereoDepth)
    stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
    stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
    stereo.setLeftRightCheck(True)          # occlusion handling
    stereo.setExtendedDisparity(True)       # min range ~20 cm at 400P
    stereo.setSubpixel(True)               # better long-range accuracy
    stereo.setDepthAlign(dai.CameraBoardSocket.CAM_B)  # align depth to left cam

    cam_left.out.link(stereo.left)
    cam_right.out.link(stereo.right)

    # ── ImageManip: resize 640×400 depth → 128×128 for CNN (1 SHAVE) ─────────
    manip = pipeline.create(dai.node.ImageManip)
    manip.initialConfig.setResize(128, 128)
    manip.initialConfig.setFrameType(dai.RawImgFrame.Type.GRAY8)
    manip.setMaxOutputFrameSize(128 * 128)
    manip.inputImage.setBlocking(False)
    manip.inputImage.setQueueSize(1)
    stereo.depth.link(manip.inputImage)

    # ── NeuralNetwork: encoder blob on MyriadX VPU (6 SHAVEs, FP16) ──────────
    nn = pipeline.create(dai.node.NeuralNetwork)
    nn.setBlobPath(blob_path)
    nn.setNumInferenceThreads(2)
    nn.input.setBlocking(False)
    nn.input.setQueueSize(1)
    manip.out.link(nn.input)

    # ── XLinkOut: encoder feature vectors ────────────────────────────────────
    xout_nn = pipeline.create(dai.node.XLinkOut)
    xout_nn.setStreamName("nn_out")
    nn.out.link(xout_nn.input)

    # ── IMU: BMI270 6-axis (accel + gyro only — no magnetometer on OAK-D Lite) ─
    imu = pipeline.create(dai.node.IMU)
    imu.enableIMUSensor([
        dai.IMUSensor.ACCELEROMETER_RAW,
        dai.IMUSensor.GYROSCOPE_RAW,
    ], reportRate=200)
    imu.setBatchReportThreshold(1)
    imu.setMaxBatchReports(10)

    xout_imu = pipeline.create(dai.node.XLinkOut)
    xout_imu.setStreamName("imu_out")
    imu.out.link(xout_imu.input)

    return pipeline, "nn_out", "imu_out"
