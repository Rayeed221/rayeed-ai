import asyncio
import sounddevice as sd
import logging

from config import SEND_SAMPLE_RATE, CHUNK_SIZE, CHANNELS, AUDIO_DEVICE_ID

logger = logging.getLogger(__name__)


def list_audio_devices():
    """
    List all available audio input devices.
    Returns dict of {device_id: device_info}.
    """
    devices = {}
    try:
        for i, device in enumerate(sd.query_devices()):
            # Only list input devices (channels > 0)
            if device.get('max_input_channels', 0) > 0:
                devices[i] = device
        return devices
    except Exception as e:
        logger.error(f"[MIC] Failed to query devices: {e}")
        return {}


def get_default_input_device():
    """
    Get the default input device ID. 
    Lists all available audio devices to the console for manual configuration.
    """
    try:
        devices = list_audio_devices()
        if not devices:
            logger.error("[MIC] No audio input devices found")
            return None

        print("\n--- Available Audio Input Devices ---")
        for dev_id, dev_info in devices.items():
            print(f"ID: {dev_id} | Name: {dev_info['name']} | Max Input Channels: {dev_info['max_input_channels']}")
        print("------------------------------------\n")

        # Fallback: use system default input device
        default_device = sd.default.device[0]  # Input device
        print(f"[MIC] System default input device ID: {default_device}")

        if default_device in devices:
            logger.info(f"[MIC] Using system default device: {default_device} - {devices[default_device]['name']}")
            return default_device

        # Fallback: use first available input device
        first_device = min(devices.keys())
        logger.info(f"[MIC] Using first available device: {first_device} - {devices[first_device]['name']}")
        return first_device
    except Exception as e:
        logger.error(f"[MIC] Error detecting input device: {e}")
        return None


class MicCapture:
    """
    Reads microphone PCM chunks into mic_queue using sounddevice.
    Checks turn_manager.is_blocked() before each enqueue —
    audio and telemetry tasks are never paused.
    
    Features:
    - Auto-detects best input device (prefers 'Microphone' name)
    - Validates device supports requested channel count
    - Fallback from mono to stereo if needed
    - Comprehensive logging for debugging
    """

    def __init__(self, mic_queue: asyncio.Queue):
        self._queue  = mic_queue
        self._stream = None
        self._device = None
        self._channels = CHANNELS

    def _select_device(self):
        """
        Select the microphone device. Priority:
        1. AUDIO_DEVICE_ID environment variable
        2. Auto-detected microphone device
        3. System default input device
        """
        if AUDIO_DEVICE_ID is not None:
            try:
                device_id = int(AUDIO_DEVICE_ID)
                device_info = sd.query_devices(device_id)
                if device_info.get('max_input_channels', 0) > 0:
                    logger.info(f"[MIC] Using device {device_id} from AUDIO_DEVICE_ID: {device_info['name']}")
                    return device_id
                else:
                    logger.warning(f"[MIC] Device {device_id} has no input channels, falling back to auto-detect")
            except (ValueError, sd.PortAudioError) as e:
                logger.warning(f"[MIC] Invalid AUDIO_DEVICE_ID {AUDIO_DEVICE_ID}: {e}, falling back to auto-detect")
        
        return get_default_input_device()

    def _validate_device_config(self):
        """
        Validate that the device supports the requested configuration.
        Falls back from mono to stereo if needed.
        """
        try:
            device_info = sd.query_devices(self._device)
            max_channels = device_info.get('max_input_channels', 0)
            
            if max_channels == 0:
                raise ValueError(f"Device {self._device} has no input channels")
            
            if self._channels > max_channels:
                logger.warning(
                    f"[MIC] Device {self._device} ({device_info['name']}) "
                    f"requested {self._channels} channels but only has {max_channels}. "
                    f"Falling back to {max_channels} channels."
                )
                self._channels = max_channels
            
            logger.info(
                f"[MIC] Device config validated: {device_info['name']} "
                f"(rate={SEND_SAMPLE_RATE}, channels={self._channels}, chunk={CHUNK_SIZE})"
            )
        except Exception as e:
            logger.error(f"[MIC] Failed to validate device config: {e}")
            raise

    async def run(self, turn_manager):
        """Start listening to microphone."""
        try:
            # Select and validate device
            self._device = self._select_device()
            if self._device is None:
                logger.error("[MIC] No input devices found")
                return
            
            self._validate_device_config()
            
            # Open stream
            logger.info(f"[MIC] Opening stream on device {self._device}...")
            self._stream = sd.InputStream(
                device=self._device,
                samplerate=SEND_SAMPLE_RATE,
                blocksize=CHUNK_SIZE,
                channels=self._channels,
                dtype='int16',
                latency='low',
            )
            self._stream.start()
            logger.info("[MIC] Listening...")
            
            try:
                while True:
                    data, overflowed = await asyncio.to_thread(
                        self._stream.read, CHUNK_SIZE
                    )
                    if overflowed:
                        logger.warning("[MIC] Buffer overflow detected (some audio frames dropped)")
                    
                    if not turn_manager.is_blocked():
                        await self._queue.put(data.tobytes())
            finally:
                self._stream.stop()
                self._stream.close()
                logger.info("[MIC] Stream closed")
        except Exception as exc:
            logger.error(f"[MIC] Fatal error: {exc}", exc_info=True)
            raise
