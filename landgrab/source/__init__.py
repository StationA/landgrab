from abc import ABCMeta


class Source(object):
    """
    Orchestrates the application of a deserialization format on the input source
    """
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
    """
    Base class for all input source implementations. This base also implements a context manager
    interface to allow implementations to initialize and clean up in a safe manner, e.g. removing
    scratch files or closing network connections.
    """
    __metaclass__ = ABCMeta

    def __enter__(self):
        """
        Initialization function before data is pulled. Note that this should always return `self`
        """
        return self

    def pull(self):
        """
        Pulls the data into a input stream. This should return a file-like object
        """
        raise NotImplementedError

    def __exit__(self, *args):
        """
        Clean-up function that is called after data is pulled, or when an error occurs while pulling
        the data
        """
        pass
