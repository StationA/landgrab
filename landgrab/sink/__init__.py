from abc import ABCMeta


class Sink(object):
    def __init__(self, sink_impl, serializer):
        self.sink_impl = sink_impl
        self.serializer = serializer

    def save(self, transformed_data):
        with self.sink_impl as sink:
            for item in transformed_data:
                serialized = self.serializer(item)
                sink.save(serialized)


class BaseSink(object):
    __metaclass__ = ABCMeta

    def __enter__(self):
        return self

    def save(self, item):
        raise NotImplementedError

    def __exit__(self, *args):
        pass
