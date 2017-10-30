from abc import ABCMeta


class Transform(object):
    def __init__(self, tasks):
        self.tasks = tasks

    def apply(self, source_data):
        for item in source_data:
            for task in self.tasks:
                item = task(item)
            yield item


class BaseTask(object):
    __metaclass__ = ABCMeta

    def __call__(self, item):
        raise NotImplementedError
