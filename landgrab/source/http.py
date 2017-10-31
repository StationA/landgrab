from urllib2 import urlopen

from landgrab.source import BaseSource


class HTTPSource(BaseSource):
    def __init__(self, uri, method='GET'):
        self.uri = uri
        self.method = method

    def __enter__(self):
        # TODO: Figure out if we can just use smart_open here instead
        self.download_stream = urlopen(self.uri)
        return self

    def pull(self):
        return self.download_stream

    def __exit__(self, *args):
        self.download_stream.close()
