import asyncio
import pyaudio
import logging

from config import RECEIVE_SAMPLE_RATE, CHANNELS

logger = logging.getLogger(__name__)
_FORMAT = pyaudio.paInt16


class Playback:
    """
    Plays AI audio chunks from audio_in_queue.
    Calls turn_manager.unblock() once the queue drains —
    re-enabling microphone input.
    """

    def __init__(self, pya: pyaudio.PyAudio, audio_queue: asyncio.Queue):
        self._pya    = pya
        self._queue  = audio_queue
        self._stream = None

    async def run(self, turn_manager):
        self._stream = await asyncio.to_thread(
            self._pya.open,
            format=_FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        try:
            while True:
                chunk = await self._queue.get()
                await asyncio.to_thread(self._stream.write, chunk)
                if self._queue.empty():
                    turn_manager.unblock()
        finally:
            self._stream.close()
