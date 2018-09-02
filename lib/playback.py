from lib import Stream

class Playback(object):
    def __init__(self, awsHelper, mixer):
        self._stream = None
        self._awsHelper = awsHelper
        self._mixer = mixer
        pass

    def play(self, streams):
        if self._queueStreams(streams):
            self._mixer.load(self._stream)
            self._mixer.play()

    def stop(self):
        if self._stream:
            self._stream.close()
            del self._stream

    def _queueStreams(self, streams):
        if not streams:
            return False

        session = self._awsHelper.getSession()
        s3 = session.client('s3', region_name='eu-central-1')

        signedUrl = s3.generate_presigned_url(
            ClientMethod = "get_object",
            ExpiresIn = 3600,
            HttpMethod = 'GET',
            Params = {
                "Bucket": "daastani",
                "Key": streams,
                }
            )

        self._stream = Stream(signedUrl)

        return True


