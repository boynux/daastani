import requests
import tempfile

class Stream(object):
    default_options = {}

    def __init__(self, url, options={}):
        self._options = self.default_options
        self._options.update(options)

        self._file = requests.get(url, stream=True)
        # self._tempfile = tempfile.NamedTemoraryFile()

    def read(self, *args):
        print('reading ...')
        if args:
            yield self._file.raw.read(args[0])
        else:
            yield self.file.raw.read()

        return generator()
    def close(self):
        self._file.close()
        # self._tempfile.close()
