from abc import ABCMeta


class Transform(object):
    """
    Orchestrates the application of zero or more transformation tasks on the source data
    """
    def __init__(self, tasks):
        self.tasks = tasks

    def apply(self, source_data):
        """
        Applies each transformation task to the source data, using the result of the task as the
        input to the next task
        """
        for item in source_data:
            for task in self.tasks:
                item = task(item)
            yield item


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
