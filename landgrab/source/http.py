import requests

from landgrab.source import BaseSource


class HTTPSource(BaseSource):
    def __init__(self, uri, method='GET', request_timeout=60 * 60 * 24):
        self.uri = uri
        self.method = method
        self.request_timeout = request_timeout

    def pull(self):
        res = requests.request(self.method, self.uri)
        return res.content
