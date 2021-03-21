import requests
import tempfile
import asyncio
import miniaudio
import time
import concurrent.futures
import threading
import os

class CachedStream(miniaudio.StreamableSource):
    DEFAULT_OPTIONS = {'encoding': 'MP3'}

    BLOCK_SIZE = 8*1024
    BUFFER_SIZE = 1024*1024

    def __init__(self, url: str, loop: object, options: dict={}):
        print('initializing ....')
        self._options = self.DEFAULT_OPTIONS
        self._options.update(options)
        self._url = url
        self._buffer = bytes()
        self._stop = False
        self._loop = loop

        self._lock = threading.Lock()
        # Srart download as soon as the stream is created, don't ask me why!
        threading.Thread(target=self._download_stream).start()

    def _download_stream(self) -> None:
        dst = self._options['dst'] if 'dst' in self._options else None

        if dst:
            f = tempfile.NamedTemporaryFile()

        with requests.get(self._url, stream=True) as result:
            for chunk in result.iter_content(chunk_size=self.BLOCK_SIZE):
                if dst:
                    f.write(chunk)
                with self._lock:
                    self._buffer += chunk
                # If buffer is full wait until it's empty to avoid zombies eating your brain
                while len(self._buffer) >= self.BUFFER_SIZE:
                    if self._stop:
                        return
                    time.sleep(0.1)

        # If we didn't get stop call we are probably at the end of stream
        if dst and not self._stop:
            f.flush()
            os.rename(f.name, dst)
        self._stop = True

    async def _readChunk(self, count) -> bytes:
        while len(self._buffer) < count and not self._stop:
            # wait for buffer
            await asyncio.sleep(0.5)

        async with self._lock:
            chunk = self._buffer[:count]
            self._buffer = self._buffer[count:]

            return chunk

    def getEncoding(self) -> miniaudio.FileFormat:
        if self._options['encoding'] == 'OGG':
            return miniaudio.FileFormat.VORBIS
        else:
            return miniaudio.FileFormat.MP3

    def read(self, count: int) -> bytes:
        # chunk = asyncio.run_coroutine_threadsafe(self._readChunk(count), self._loop).result()
        # future = self._loop.create_task(self._readChunk(count))
        # self._loop.run_until_complete(future)
        while len(self._buffer) < count and not self._stop:
            # wait for buffer
            time.sleep(0.2)

        with self._lock:
            chunk = self._buffer[:count]
            self._buffer = self._buffer[count:]

        return chunk

    def close(self):
        self.stop = True
