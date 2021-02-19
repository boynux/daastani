import miniaudio
import asyncio
import os
import time

from lib import Stream

class Playback(object):
    def __init__(self, awsHelper, mixer):
        self._stream = None
        self._awsHelper = awsHelper
        self._mixer = mixer
        self._player = None
        self._source = None
        self._stop = False
        self._device = miniaudio.PlaybackDevice()


    def samples_path(self, filename):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'samples', filename)

    def play(self, streams):
        encoding = miniaudio.FileFormat.MP3
        ext = streams.split('.')[-1]
        if ext.lower() == 'ogg':
            encoding = miniaudio.FileFormat.VORBIS

        url =  self._queueStreams(streams)
        if url:
            self._source = miniaudio.IceCastClient(url)
            stream = miniaudio.stream_any(self._source, encoding)
            # stream = miniaudio.stream_file(self.samples_path("music.mp3"))
            print('playing ...')
            self._device.start(stream)
                
            # self._mixer.load(self._stream)
            # self._mixer.play()

    def stop(self):
        print('stopping ...')
        if self._device:
            self._device.stop()

        if self._source:
            self._source.close()
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
        self._stream = Stream(signedUrl)

        return signedUrl
