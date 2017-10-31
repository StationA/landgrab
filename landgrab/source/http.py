from urllib2 import urlopen

from landgrab.source import BaseSource


class HTTPSource(BaseSource):
    """
    An input source for HTTP-based network data
    """
    def __init__(self, uri, method='GET'):
        self.uri = uri
        self.method = method

    def __enter__(self):
        # TODO: Figure out if we can just use smart_open here instead
        # TODO: Figure out how to support different methods
        self.download_stream = urlopen(self.uri)
        return self

    def pull(self):
        return self.download_stream

    def __exit__(self, *args):
        self.download_stream.close()
