#!/usr/bin/env python3
import sys
import os
import sounddevice as sd
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

ENV_FILE = ".env"

def get_devices():
    """Get all devices and filter input devices."""
    devices = sd.query_devices()
    input_devices = {i: d for i, d in enumerate(devices) if d.get('max_input_channels', 0) > 0}
    return devices, input_devices

def save_device_id(device_id):
    """Save the selected device ID to the .env file."""
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()

    new_lines = []
    found = False
    for line in lines:
        if line.startswith("AUDIO_DEVICE_ID="):
            new_lines.append(f"AUDIO_DEVICE_ID={device_id}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"AUDIO_DEVICE_ID={device_id}\n")

    with open(ENV_FILE, 'w') as f:
        f.writelines(new_lines)
    print(f"\n[INFO] Saved AUDIO_DEVICE_ID={device_id} to {ENV_FILE}")

def main():
    while True:
        print("\n=== Audio Device Manager ===")
        all_devs, input_devs = get_devices()
        
        print("\nAvailable Input Devices:")
        for idx, dev in input_devs.items():
            print(f"[{idx}] {dev['name']}")
            
        print("\nOptions:")
        print("  [s] Scan/Refresh")
        print("  [#] Enter ID to select device")
        print("  [q] Quit")
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 's':
            continue
        else:
            try:
                device_id = int(choice)
                if device_id in input_devs:
                    print(f"\nSelected: {input_devs[device_id]['name']}")
                    confirm = input("Save this device? (y/n): ").strip().lower()
                    if confirm == 'y':
                        save_device_id(device_id)
                        break
                else:
                    print("\n[ERROR] Invalid device ID.")
            except ValueError:
                print("\n[ERROR] Invalid choice.")

if __name__ == "__main__":
    main()
