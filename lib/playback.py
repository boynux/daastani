import miniaudio
import asyncio
import os
import time

from lib import CachedStream

class Playback(object):
    def __init__(self, awsHelper, cache):
        self._awsHelper = awsHelper
        self._device = miniaudio.PlaybackDevice()

    def data_path(self, filename):
        return os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../'), 'data', filename)

    def get_encoding(self, filename):
        encoding = miniaudio.FileFormat.MP3
        ext = filename.split('.')[-1]
        if ext.lower() == 'ogg':
            encoding = miniaudio.FileFormat.VORBIS

        return encoding

    def get_stream(self, streams: object):
        if isinstance(streams, miniaudio.StreamableSource):
            return miniaudio.stream_any(streams, streams.getEncoding())
        if os.path.isfile(streams):
            return miniaudio.stream_file(streams)
        elif os.path.isfile(self.data_path(streams)):
            return miniaudio.stream_file(self.data_path(streams))
        else:
            url =  self._queueStreams(streams)
            if url:
                self._source = miniaudio.IceCastClient(url)
                return miniaudio.stream_any(self._source, self.get_encoding(streams))
            return None

    async def play(self, streams):
        stream = self.get_stream(streams)
        if stream:
            print('playing ...')
            self._device.start(stream)
                
    async def stop(self):
        print('stopping ...')
        if self._device:
            self._device.stop()

    def _queueStreams(self, streams):
        if not streams:
            return False

        session = self._awsHelper.getSession()
        s3 = session.client('s3', region_name='eu-central-1')

        signedUrl = s3.generate_presigned_url(
            ClientMethod="get_object",
            ExpiresIn=1800,
            HttpMethod='GET',
            Params={
                "Bucket": "daastani",
                "Key": streams,
            }
        )

        print(signedUrl)
        self._stream = CachedStream(signedUrl)

        return signedUrl
