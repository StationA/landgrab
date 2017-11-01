import tempfile
import urllib

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
        self.f = tempfile.NamedTemporaryFile(delete=True)
        urllib.urlretrieve(self.uri, self.f.name)
        return self

    def pull(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()
        urllib.urlcleanup()
