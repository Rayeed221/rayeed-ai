#!/usr/bin/env python3
"""
Diagnostic script to test microphone device detection and audio capture.
Run this to see which devices are available and which one is being used.
"""

import sounddevice as sd
import numpy as np
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SEND_SAMPLE_RATE, CHUNK_SIZE, CHANNELS, AUDIO_DEVICE_ID
from audio.mic_capture import list_audio_devices, get_default_input_device


def show_all_devices():
    """Display all available audio devices."""
    print("\n" + "="*70)
    print("ALL AUDIO DEVICES")
    print("="*70)
    try:
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            marker = "✓ INPUT" if device.get('max_input_channels', 0) > 0 else "  OUTPUT"
            print(f"[{i:2d}] {marker} | {device['name']}")
            print(f"       Channels: {device.get('max_input_channels', 0)} in, "
                  f"{device.get('max_output_channels', 0)} out")
            print(f"       Rate: {device.get('default_samplerate', 'N/A')} Hz")
            print()
    except Exception as e:
        print(f"ERROR querying devices: {e}")


def show_input_devices():
    """Display only input devices."""
    print("\n" + "="*70)
    print("INPUT DEVICES (Microphones)")
    print("="*70)
    devices = list_audio_devices()
    if not devices:
        print("ERROR: No input devices found!")
        return
    
    for dev_id, dev_info in devices.items():
        print(f"[{dev_id}] {dev_info['name']}")
        print(f"    Channels: {dev_info.get('max_input_channels', 0)}")
        print(f"    Default Rate: {dev_info.get('default_samplerate', 'N/A')} Hz")
        print()


def show_selected_device():
    """Show which device will be used."""
    print("\n" + "="*70)
    print("SELECTED DEVICE")
    print("="*70)
    
    if AUDIO_DEVICE_ID is not None:
        print(f"AUDIO_DEVICE_ID env var set: {AUDIO_DEVICE_ID}")
        try:
            device_id = int(AUDIO_DEVICE_ID)
            device_info = sd.query_devices(device_id)
            print(f"Device {device_id}: {device_info['name']}")
            print(f"  Channels: {device_info.get('max_input_channels', 0)}")
        except Exception as e:
            print(f"ERROR: Invalid device ID: {e}")
    else:
        device_id = get_default_input_device()
        if device_id is not None:
            device_info = sd.query_devices(device_id)
            print(f"Auto-detected: Device {device_id}")
            print(f"  Name: {device_info['name']}")
            print(f"  Channels: {device_info.get('max_input_channels', 0)}")
        else:
            print("ERROR: Could not auto-detect device!")


def test_capture(device_id, duration=3, sample_rate=16000, channels=1):
    """Test audio capture on specified device."""
    print(f"\n{'='*70}")
    print(f"TESTING AUDIO CAPTURE")
    print(f"{'='*70}")
    print(f"Device: {device_id}")
    print(f"Duration: {duration}s, Sample Rate: {sample_rate} Hz, Channels: {channels}")
    print(f"\nSpeaking now... (you should see audio levels below)")
    print("-" * 70)
    
    try:
        with sd.InputStream(
            device=device_id,
            samplerate=sample_rate,
            blocksize=2048,
            channels=channels,
            dtype='int16',
            latency='low'
        ) as stream:
            frames_captured = 0
            max_level = 0
            
            for _ in range(int(sample_rate * duration / 2048)):
                data, overflow = stream.read(2048)
                if overflow:
                    print("  ⚠ OVERFLOW (buffer full, audio dropped)")
                
                # Calculate audio level (RMS)
                level = np.sqrt(np.mean(data ** 2))
                max_level = max(max_level, level)
                
                # Show level bar
                bar_length = int(level / 1000)
                bar = '█' * min(bar_length, 50)
                print(f"  [{bar:<50}] {level:.0f}")
                
                frames_captured += 1
            
            print(f"\nMax audio level: {max_level:.0f}")
            if max_level < 100:
                print("⚠ WARNING: Very low audio level detected! Check microphone:")
                print("  1. Is the microphone muted?")
                print("  2. Is the microphone properly connected?")
                print("  3. Is the input volume too low in system settings?")
            elif max_level < 1000:
                print("⚠ WARNING: Low audio level. You may need to increase microphone gain.")
            else:
                print("✓ Audio capture working!")
                
    except Exception as e:
        print(f"ERROR during capture: {e}")


def main():
    print("\n🎤 MICROPHONE DIAGNOSTIC TOOL 🎤")
    print("This will help identify microphone issues.\n")
    
    # Show all info
    show_all_devices()
    show_input_devices()
    show_selected_device()
    
    # Test capture if device found
    device_id = AUDIO_DEVICE_ID
    if device_id is None:
        device_id = get_default_input_device()
    
    if device_id is not None:
        test_capture(device_id, duration=3)
    else:
        print("\n❌ ERROR: Could not find any input device!")
        print("Possible solutions:")
        print("  1. Restart the application after plugging in microphone")
        print("  2. Check system audio settings")
        print("  3. Try: AUDIO_DEVICE_ID=0 python app.py (or other device number from list)")


if __name__ == "__main__":
    main()
