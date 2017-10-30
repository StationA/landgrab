from abc import ABCMeta


class Source(object):
    def __init__(self, source_impl, deserializer, license=None):
        self.source_impl = source_impl
        self.deserializer = deserializer
        self.license = license

    def pull(self):
        with self.source_impl as source:
            raw = source.pull()
            for item in self.deserializer(raw):
                yield item


class BaseSource(object):
    __metaclass__ = ABCMeta

    def __enter__(self):
        return self

    def pull(self):
        raise NotImplementedError

    def __exit__(self, *args):
        pass
