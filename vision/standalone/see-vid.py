import os
import cv2
import csv
import glob
import numpy as np

BASE_DIR = "continuous_embedded_recordings"
FPS = 30
IMU_RATE = 400

def get_latest_chunk_dir(base_dir):
    """Finds the most recently created chunk directory within the base folder."""
    if not os.path.exists(base_dir):
        print(f"[ERROR] Base directory '{base_dir}' does not exist.")
        return None
    
    # Get all subdirectories starting with 'chunk_'
    chunks = glob.glob(os.path.join(base_dir, "chunk_*"))
    if not chunks:
        print(f"[ERROR] No recording chunks found in '{base_dir}'.")
        return None
    
    # Sort by name (which contains the timestamp) and return the latest
    chunks.sort()
    return chunks[-1]

def load_imu_data(csv_path):
    """Loads IMU data from CSV and calculates relative timestamps for synchronization."""
    imu_data = []
    if not os.path.exists(csv_path):
        print(f"[WARNING] IMU CSV not found at {csv_path}")
        return imu_data

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        first_ts = None
        for row in reader:
            ts = float(row["timestamp_ms"])
            if first_ts is None:
                first_ts = ts
            
            # Store data with a normalized timestamp starting at 0.0 seconds
            imu_data.append({
                "rel_time_sec": (ts - first_ts) / 1000.0,
                "accel": (float(row["accel_x"]), float(row["accel_y"]), float(row["accel_z"])),
                "gyro": (float(row["gyro_x"]), float(row["gyro_y"]), float(row["gyro_z"]))
            })
    return imu_data

def draw_telemetry(frame, imu_reading):
    """Overlays IMU accelerometer and gyroscope data onto the video frame."""
    if not imu_reading:
        return frame

    ax, ay, az = imu_reading["accel"]
    gx, gy, gz = imu_reading["gyro"]

    # Text overlay settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color = (0, 255, 0) # Green text
    thickness = 2
    x_offset = 20
    y_offset = 40

    texts = [
        f"Accel (m/s^2): X:{ax:.2f} Y:{ay:.2f} Z:{az:.2f}",
        f"Gyro (rad/s): X:{gx:.2f} Y:{gy:.2f} Z:{gz:.2f}"
    ]

    for i, text in enumerate(texts):
        # Draw black background shadow for better readability
        cv2.putText(frame, text, (x_offset + 2, y_offset + (i * 30) + 2), font, font_scale, (0, 0, 0), thickness + 1)
        # Draw actual text
        cv2.putText(frame, text, (x_offset, y_offset + (i * 30)), font, font_scale, color, thickness)
        
    return frame

def main():
    latest_chunk = get_latest_chunk_dir(BASE_DIR)
    if not latest_chunk:
        return

    print(f"[INFO] Visualizing data from: {latest_chunk}")

    rgb_path = os.path.join(latest_chunk, "rgb_video.h265")
    depth_path = os.path.join(latest_chunk, "depth_disparity.h265")
    imu_path = os.path.join(latest_chunk, "imu_raw_6dof.csv")

    # Load media sources
    # Note: OpenCV handles raw .h265 bitstreams natively in most modern installations.
    cap_rgb = cv2.VideoCapture(rgb_path)
    cap_depth = cv2.VideoCapture(depth_path)
    imu_data = load_imu_data(imu_path)

    if not cap_rgb.isOpened() or not cap_depth.isOpened():
        print("[ERROR] Failed to open video streams. Ensure OpenCV is built with FFmpeg support.")
        return

    # Tracking variables for synchronization
    frame_idx = 0
    imu_idx = 0
    total_imu = len(imu_data)

    print("[INFO] Playing back streams. Press 'q' or 'ESC' to exit, 'Space' to pause.")

    while True:
        ret_rgb, frame_rgb = cap_rgb.read()
        ret_depth, frame_depth = cap_depth.read()

        # Break if either video ends
        if not ret_rgb or not ret_depth:
            print("[INFO] End of recording reached.")
            break

        # Calculate expected video timestamp
        current_video_time = frame_idx / FPS

        # Synchronize IMU pointer to match the video timeline
        current_imu = None
        while imu_idx < total_imu and imu_data[imu_idx]["rel_time_sec"] <= current_video_time:
            current_imu = imu_data[imu_idx]
            imu_idx += 1

        # Process Depth Frame: H.265 decodes to a BGR image by default in OpenCV.
        # We must convert the 8-bit disparity back to grayscale before applying a colormap.
        depth_gray = cv2.cvtColor(frame_depth, cv2.COLOR_BGR2GRAY)
        
        # --- FIX: Scale Disparity to full 0-255 range ---
        # The OAK hardware outputs disparity values from 0 to 95 by default.
        # Without scaling, the colormap only uses the bottom 40% of its colors, making it look dark/inaccurate.
        # Multiplying by (255/95) stretches the data so the closest objects become bright red.
        depth_scaled = cv2.convertScaleAbs(depth_gray, alpha=(255.0 / 95.0))
        
        # Apply Jet colormap to visualize depth (closer = red, further = blue)
        depth_colored = cv2.applyColorMap(depth_scaled, cv2.COLORMAP_JET)

        # Overlay telemetry on the RGB frame
        frame_rgb = draw_telemetry(frame_rgb, current_imu)

        # Standardize heights to concatenate frames side-by-side
        target_height = 540 # Half of 1080p for comfortable viewing
        
        # Calculate proportional widths
        rgb_h, rgb_w = frame_rgb.shape[:2]
        depth_h, depth_w = depth_colored.shape[:2]
        
        rgb_target_w = int((target_height / rgb_h) * rgb_w)
        depth_target_w = int((target_height / depth_h) * depth_w)

        frame_rgb_resized = cv2.resize(frame_rgb, (rgb_target_w, target_height))
        frame_depth_resized = cv2.resize(depth_colored, (depth_target_w, target_height))

        # Concatenate horizontally
        combined_frame = np.hstack((frame_rgb_resized, frame_depth_resized))

        # Display the result
        cv2.imshow("DepthAI Spatial Playback (RGB + Depth + IMU)", combined_frame)

        # Dynamic playback control (approximating 30 FPS delay)
        key = cv2.waitKey(int(1000 / FPS)) & 0xFF
        if key == ord('q') or key == 27: # 'q' or ESC
            break
        elif key == 32: # Spacebar to pause
            print("[INFO] Paused. Press Space to resume.")
            while True:
                resume_key = cv2.waitKey(0) & 0xFF
                if resume_key == 32:
                    break
                if resume_key == ord('q') or resume_key == 27:
                    cap_rgb.release()
                    cap_depth.release()
                    cv2.destroyAllWindows()
                    return

        frame_idx += 1

    # Cleanup resources
    cap_rgb.release()
    cap_depth.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()