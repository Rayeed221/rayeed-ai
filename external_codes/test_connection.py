import time
from pymavlink import mavutil

def connect_pixhawk():
    # GPIO 14/15 maps to /dev/ttyAMA0 on the Raspberry Pi
    # Default baud rate for Pixhawk telemetry ports is usually 57600
    serial_port = '/dev/ttyAMA0'
    baud_rate = 115200

    print(f"Connecting to Pixhawk on {serial_port} at {baud_rate} baud...")
    
    try:
        # Create the connection
        master = mavutil.mavlink_connection(serial_port, baud=baud_rate)
        
        # Wait for the first heartbeat 
        # This confirms the Pi is successfully receiving data from the Pixhawk
        print("Waiting for heartbeat...")
        master.wait_heartbeat()
        print(f"Heartbeat received from system (system {master.target_system} component {master.target_component})")
        
        return master
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def request_data(master):
    """Example function to continuously read messages from Pixhawk"""
    while True:
        try:
            # Grab any message that arrives
            msg = master.recv_match(blocking=True, timeout=1.0)
            if not msg:
                continue
                
            # Filter for specific messages, e.g., ATTITUDE (roll, pitch, yaw)
            if msg.get_type() == 'ATTITUDE':
                print(f"Roll: {msg.roll:.2f}, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")
                
            # Or global position
            elif msg.get_type() == 'GLOBAL_POSITION_INT':
                print(f"Lat: {msg.lat / 1e7}, Lon: {msg.lon / 1e7}, Alt: {msg.alt / 1000}m")
            time.sleep(0.1)  # Adjust sleep time as needed for your application
        except KeyboardInterrupt:
            print("\nDisconnecting...")
            break

if __name__ == "__main__":
    mav_connection = connect_pixhawk()
    if mav_connection:
        request_data(mav_connection)
