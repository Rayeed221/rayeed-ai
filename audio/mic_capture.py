import asyncio
import pyaudio
import logging

from config import SEND_SAMPLE_RATE, CHUNK_SIZE, CHANNELS

logger = logging.getLogger(__name__)
_FORMAT = pyaudio.paInt16


class MicCapture:
    """
    Reads microphone PCM chunks into mic_queue.
    Checks turn_manager.is_blocked() before each enqueue —
    audio and telemetry tasks are never paused.
    """

    def __init__(self, pya: pyaudio.PyAudio, mic_queue: asyncio.Queue):
        self._pya    = pya
        self._queue  = mic_queue
        self._stream = None

    async def run(self, turn_manager):
        mic_info = self._pya.get_default_input_device_info()
        self._stream = await asyncio.to_thread(
            self._pya.open,
            format=_FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        logger.info("[MIC] Listening...")
        try:
            while True:
                data = await asyncio.to_thread(
                    self._stream.read, CHUNK_SIZE, exception_on_overflow=False
                )
                if not turn_manager.is_blocked():
                    await self._queue.put(data)
        finally:
            self._stream.close()
