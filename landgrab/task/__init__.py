from abc import ABCMeta


class BaseTask(object):
    """
    Base interface for all transformation tasks
    """
    __metaclass__ = ABCMeta

    def __call__(self, item):
        """
        Function that should return the transformed item
        """
        raise NotImplementedError
