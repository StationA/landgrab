from abc import ABCMeta


class Sink(object):
    def __init__(self, sink_impl, serializer):
        self.sink_impl = sink_impl
        self.serializer = serializer

    def save(self, transformed_data):
        transformed_data.map(self.serializer).to_textfiles('/tmp/test-*.jsonlines')


class BaseSink(object):
    __metaclass__ = ABCMeta

    def __enter__(self):
        return self

    def save(self, item):
        raise NotImplementedError

    def __exit__(self, *args):
        pass
