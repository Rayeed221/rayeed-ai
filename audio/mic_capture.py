import asyncio
import numpy as np
import sounddevice as sd
import logging

from config import SEND_SAMPLE_RATE, CHUNK_SIZE, CHANNELS

logger = logging.getLogger(__name__)


class MicCapture:
    """
    Reads microphone PCM chunks into mic_queue using sounddevice.
    Checks turn_manager.is_blocked() before each enqueue —
    audio and telemetry tasks are never paused.
    """

    def __init__(self, mic_queue: asyncio.Queue):
        self._queue  = mic_queue
        self._stream = None

    async def run(self, turn_manager):
        self._stream = sd.InputStream(
            samplerate=SEND_SAMPLE_RATE,
            blocksize=CHUNK_SIZE,
            channels=CHANNELS,
            dtype='int16',
        )
        self._stream.start()
        logger.info("[MIC] Listening...")
        try:
            while True:
                data, _overflowed = await asyncio.to_thread(
                    self._stream.read, CHUNK_SIZE
                )
                if not turn_manager.is_blocked():
                    await self._queue.put(data.tobytes())
        finally:
            self._stream.stop()
            self._stream.close()
