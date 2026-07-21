import os
import csv
import time
from datetime import datetime
import depthai as dai

FPS = 30
CHUNK_DURATION_SEC = 120  # Segment directory rotation threshold (2 minutes)
BASE_OUTPUT_DIR = "continuous_embedded_recordings"

class ChunkManager:
    """Handles continuous file rotation without dropping hardware frames."""
    def __init__(self, base_folder):
        self.base_folder = base_folder
        self.rgb_file = None
        self.depth_file = None
        self.csv_file = None
        self.csv_writer = None
        self.start_time = 0
        os.makedirs(self.base_folder, exist_ok=True)

    def rotate_chunk(self):
        """Safely closes existing file descriptors and transitions logging to a new directory."""
        self.close_files()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_dir = os.path.join(self.base_folder, f"chunk_{timestamp}")
        os.makedirs(current_dir, exist_ok=True)
        print(f"\n[INFO] Threshold reached. Transitioning data payload into: {current_dir}/")

        # Open in binary write ('wb') to dump raw H.265 bitstream directly
        self.rgb_file = open(os.path.join(current_dir, "rgb_video.h265"), 'wb')
        self.depth_file = open(os.path.join(current_dir, "depth_disparity.h265"), 'wb')
        
        # Open CSV for structured 6-DoF data
        self.csv_file = open(os.path.join(current_dir, "imu_raw_6dof.csv"), mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["timestamp_ms", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"])
        
        self.start_time = time.time()

    def close_files(self):
        """Flushes buffers and clears locks."""
        if self.rgb_file: self.rgb_file.close()
        if self.depth_file: self.depth_file.close()
        if self.csv_file: self.csv_file.close()

if __name__ == "__main__":
    print("Initializing embedded v3 spatial pipeline...")
    
    chunker = ChunkManager(BASE_OUTPUT_DIR)
    
    # In DepthAI v3, we manage the device automatically via the Pipeline context manager
    with dai.Pipeline() as pipeline:
        
        # .build() cleanly initializes standard parameters in v3
        camRgb = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
        # Directly request NV12 format output needed by the hardware encoder
        rgb_output = camRgb.requestOutput((1920, 1080), type=dai.ImgFrame.Type.NV12, fps=FPS)

        enc_rgb = pipeline.create(dai.node.VideoEncoder)
        enc_rgb.setDefaultProfilePreset(FPS, dai.VideoEncoderProperties.Profile.H265_MAIN)
        rgb_output.link(enc_rgb.input)
        # v3 magic: creating an output queue directly from the port implicitly generates the XLinkOut bridges
        q_rgb = enc_rgb.bitstream.createOutputQueue(maxSize=30, blocking=False)

        monoLeft = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B, sensorFps=FPS)
        monoRight = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C, sensorFps=FPS)

        stereo = pipeline.create(dai.node.StereoDepth)
        stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.FAST_DENSITY)
        stereo.setLeftRightCheck(True)
        # Explicitly disable subpixel mode to guarantee an 8-bit disparity output
        # required by the H.265 Hardware Encoder
        stereo.setSubpixel(False)

        monoLeft.requestFullResolutionOutput().link(stereo.left)
        monoRight.requestFullResolutionOutput().link(stereo.right)

        # Disparity is inherently 8-bit, making it perfectly compatible for H.265 edge encoding
        enc_depth = pipeline.create(dai.node.VideoEncoder)
        enc_depth.setDefaultProfilePreset(FPS, dai.VideoEncoderProperties.Profile.H265_MAIN)
        stereo.disparity.link(enc_depth.input)
        q_depth = enc_depth.bitstream.createOutputQueue(maxSize=30, blocking=False)

        imu = pipeline.create(dai.node.IMU)
        imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, 400)
        imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, 400)
        imu.setBatchReportThreshold(1)
        imu.setMaxBatchReports(10)
        q_imu = imu.out.createOutputQueue(maxSize=50, blocking=False)

        print("Pipeline built successfully. Connecting and executing...")
        
        # Initialize the first data chunk directly before boot
        chunker.rotate_chunk()
        
        # Starts the unified v3 system
        pipeline.start()
        
        try:
            print("Connected. Logging raw streams... (Press 'Ctrl+C' to stop)")
            
            while pipeline.isRunning():
                # 1. Chunk boundary rotation check
                if (time.time() - chunker.start_time) >= CHUNK_DURATION_SEC:
                    chunker.rotate_chunk()

                # 2. Extract and flush H.265 RGB Bitstream to disk
                in_rgb = q_rgb.tryGet()
                if in_rgb is not None:
                    # In headless mode, we pull the direct memory buffer and push it to storage
                    in_rgb.getData().tofile(chunker.rgb_file)

                # 3. Extract and flush H.265 Depth Disparity Bitstream to disk
                in_depth = q_depth.tryGet()
                if in_depth is not None:
                    in_depth.getData().tofile(chunker.depth_file)

                # 4. Unpack 400Hz IMU Data Packets
                in_imu = q_imu.tryGet()
                if in_imu is not None:
                    for imu_packet in in_imu.packets:
                        accel = imu_packet.acceleroMeter
                        gyro = imu_packet.gyroscope
                        
                        # Generate normalized, reliable device timestamps 
                        ts = accel.getTimestamp().total_seconds() * 1000.0 
                        
                        chunker.csv_writer.writerow([
                            ts,
                            accel.x, accel.y, accel.z,
                            gyro.x, gyro.y, gyro.z
                        ])

        except KeyboardInterrupt:
            print("\nInterrupt received. Safely closing data streams...")
        finally:
            chunker.close_files()
            print(f"Recording sequence successfully terminated. Data indexed in: {BASE_OUTPUT_DIR}/")