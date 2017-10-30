from abc import ABCMeta


class BaseFormat(object):
    """
    Base class for all input/output formats
    """
    __metaclass__ = ABCMeta

    def serialize(self, item):
        pass

    def deserialize(self, raw):
        pass
