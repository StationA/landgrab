from landgrab.sink import BaseSink


class FileSink(BaseSink):
    def __init__(self, uri):
        self.fn = uri[len('file://'):]

    def __enter__(self):
        self.f = open(self.fn, 'w')
        return self

    def save(self, item):
        self.f.write(item)

    def __exit__(self, *args):
        self.f.close()
