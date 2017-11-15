from abc import ABCMeta


class Sink(object):
    def __init__(self, sink_impl, serializer):
        self.sink_impl = sink_impl
        self.serializer = serializer

    def serialized_data(self, transformed_data):
        for item in transformed_data:
            yield self.serializer(item)

    def save(self, transformed_data):
        with self.sink_impl as sink:
            sink.save_stream(self.serialized_data(transformed_data))


class BaseSink(object):
    __metaclass__ = ABCMeta

    def __enter__(self):
        return self

    def save_stream(self, items):
        for item in items:
            self.save(item)

    def save(self, item):
        raise NotImplementedError

    def __exit__(self, *args):
        pass
