from abc import ABCMeta
from multiprocessing import cpu_count


def run_tasks(item, tasks):
    for task in tasks:
        item = task(item)
        if item is None:
            break
    if item is not None:
        return item


class Transform(object):
    """
    Orchestrates the application of zero or more transformation tasks on the source data
    """
    def __init__(self, tasks=[], max_num_workers=None):
        self.tasks = tasks
        self.max_num_workers = max_num_workers if max_num_workers is not None else cpu_count()

    def apply(self, source_data):
        """
        Applies each transformation task to the source data, using the result of the task as the
        input to the next task
        """
        repartitioned = source_data.repartition(self.max_num_workers)
        transformed = repartitioned.map(run_tasks, self.tasks)
        return transformed


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
