from landgrab.source import BaseSource


class FileSource(BaseSource):
    """
    An input source for local files
    """
    def __init__(self, uri):
        self.fn = uri[len('file://'):]

    def __enter__(self):
        self.f = open(self.fn)
        return self

    def pull(self):
        return self.f

    def __exit__(self, *args):
        return self.f.close()
