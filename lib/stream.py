import requests

class Stream(object):
    default_options = {}

    def __init__(self, url, options = {}):
        self._url = url
        self._buffer = ''
        self._position = 0

        self._options = self.default_options
        self._options.update(options)

        self._file = requests.get(url, stream=True)

    def read(self, *args):
        if args:
            return self._file.raw.read(args[0])
        else:
            return self.file.raw.read()

    def close(self):
        self._file.close()
