from pymavlink import mavutil
import time

# --- CONFIG ---
TCP_ENDPOINT = "tcp:127.0.0.1:5763"
REQUEST_RATE_HZ = 50  # high-rate streaming

# --- CONNECT ---
master = mavutil.mavlink_connection(TCP_ENDPOINT)
master.wait_heartbeat()
print(f"Connected to system {master.target_system}")

# --- SET STREAM RATE (ArduCopter 4.6.x compatible) ---
def set_stream_rate(rate_hz):
    master.mav.request_data_stream_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        rate_hz,
        1
    )

set_stream_rate(REQUEST_RATE_HZ)

# --- OPTIONAL: PARAM TUNING FOR LOW LATENCY ---
def set_param(name, value):
    master.mav.param_set_send(
        master.target_system,
        master.target_component,
        name.encode('utf-8'),
        float(value),
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )

# Example latency-sensitive params (adjust if needed)
# set_param("SR0_EXTRA1", REQUEST_RATE_HZ)
# set_param("SR0_POSITION", REQUEST_RATE_HZ)
# set_param("SR0_RAW_SENS", REQUEST_RATE_HZ)

# --- MESSAGE FILTER SET ---
TRACKED_MSGS = {
    "HEARTBEAT",
    "SYSTEM_TIME",
    "TIMESYNC",
    "ATTITUDE",
    "ATTITUDE_QUATERNION",
    "HIGHRES_IMU",
    "SCALED_IMU",
    "LOCAL_POSITION_NED",
    "GLOBAL_POSITION_INT",
    "GPS_RAW_INT",
    "VFR_HUD",
    "ALTITUDE",
    "BATTERY_STATUS",
    "SYS_STATUS",
    "EXTENDED_SYS_STATE",
    "HOME_POSITION",
    "POSITION_TARGET_LOCAL_NED",
    "POSITION_TARGET_GLOBAL_INT",
    "NAV_CONTROLLER_OUTPUT",
    "MISSION_CURRENT",
    "RC_CHANNELS",
    "SERVO_OUTPUT_RAW",
    "ACTUATOR_OUTPUT_STATUS",
    "ESTIMATOR_STATUS",
    "ODOMETRY",
    "VISION_POSITION_ESTIMATE",
    "VISION_SPEED_ESTIMATE",
    "DISTANCE_SENSOR",
    "OBSTACLE_DISTANCE",
    "TRAJECTORY_REPRESENTATION_WAYPOINTS",
    "UTM_GLOBAL_POSITION",
}

# --- LOW LATENCY LOOP ---
while True:
    msg = master.recv_match(blocking=True, timeout=0.01)
    if not msg:
        continue

    msg_type = msg.get_type()

    if msg_type in TRACKED_MSGS:
        ts = time.time()
        print(f"[{ts:.6f}] {msg_type}: {msg.to_dict()}")
