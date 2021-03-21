""" Uses filesystem cache to decorate the player """
import asyncio
import os
import tempfile
import time
import shutil

from lib import CredentialsProvider, Playback, CachedStream

class Cache(object):
    def __init__(self, awsHelper: CredentialsProvider, target: Playback, loop: object) -> None:
        self._target = target
        self._awsHelper = awsHelper
        self._eventLoop = loop
        self._futures = []

    def cache_path(self, filename: str) -> str:
        return os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../'), 'data/cache', filename)
    
    def data_path(self, filename: str) -> str:
        return os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../'), 'data', filename)
    
    def _getCahcedFilename(self, filename: str) -> str:
        if os.path.isfile(self.cache_path(filename)):
            return self.cache_path(filename)
        elif os.path.isfile(self.data_path(filename)):
            return self.data_path(filename)
        else:
            # Assuming the file should be downloaded from s3
            url =  self._sign(filename)
            if url:
                # return self._cache(filename, url)
                return CachedStream(url, self._eventLoop, options={'dst': self.cache_path(filename)})
                
        return None


    async def _stream(self, url: str, tmp: object, dst: str):
        stream = CachedStream(url, loop=self._eventLoop).read()

        for chunk in stream:
            tmp.write(chunk)

        tmp.close()

        # this is remporary hack to mvoe the file to cache without interupting the playback
        # ideally we should wait until playback is done or stopped and them move the file ....

        f = tempfile.NamedTemporaryFile(delete=False)
        shutil.copyfile(tmp.name, f.name)
        os.rename(f.name, dst)
        f.close()

    def _cache(self, filename: str, url: str) -> str:
        s = filename.split('.')[-1]
        f = tempfile.NamedTemporaryFile(suffix=f'.{s}', delete=False, buffering=0)

        self._futures += [self._eventLoop.create_task(self._stream(url, f, self.cache_path(filename)))]

        return f.name

    async def play(self, filename):
        await self._target.play(self._getCahcedFilename(filename))

    async def stop(self):
        await self._target.stop()

    def _sign(self, s3Key):
        if not s3Key:
            return False

        session = self._awsHelper.getSession()
        s3 = session.client('s3', region_name='eu-central-1')

        signedUrl = s3.generate_presigned_url(
            ClientMethod="get_object",
            ExpiresIn=1800,
            HttpMethod='GET',
            Params={
                "Bucket": "daastani",
                "Key": s3Key,
            }
        )

        print(signedUrl)

        return signedUrl
