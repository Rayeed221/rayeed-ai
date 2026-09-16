import asyncio
import numpy as np
import sounddevice as sd
import logging

from config import RECEIVE_SAMPLE_RATE, CHANNELS, AUDIO_OUTPUT_LATENCY

logger = logging.getLogger(__name__)


def _output_latency():
    """AUDIO_OUTPUT_LATENCY as a float (seconds) or a PortAudio hint string."""
    try:
        return float(AUDIO_OUTPUT_LATENCY)
    except (TypeError, ValueError):
        return AUDIO_OUTPUT_LATENCY


class Playback:
    """
    Plays AI audio chunks from audio_in_queue using sounddevice.
    Calls turn_manager.unblock() once the queue drains —
    re-enabling microphone input.
    """

    def __init__(self, audio_queue: asyncio.Queue):
        self._queue  = audio_queue
        self._stream = None

    async def run(self, turn_manager):
        # PortAudio defaults to latency='high' (~100 ms+ of output buffering
        # on a Pi), which is added to every AI reply.  Override via
        # AUDIO_OUTPUT_LATENCY=high if the board underruns and crackles.
        self._stream = sd.OutputStream(
            samplerate=RECEIVE_SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
            latency=_output_latency(),
        )
        self._stream.start()
        try:
            while True:
                chunk = await self._queue.get()
                data = np.frombuffer(chunk, dtype='int16')
                await asyncio.to_thread(self._stream.write, data)
                if self._queue.empty():
                    turn_manager.unblock()
        finally:
            self._stream.stop()
            self._stream.close()
