import dask
import dask.bag as db
from dask.delayed import delayed

from landgrab.config import create_sink, create_source, create_task, get_deserializer, \
                            get_serializer, DEFAULT_FORMAT
from landgrab.sink import Sink
from landgrab.source import Source
from landgrab.transform import Transform


def _create_sink(sink_cfg):
    sink_impl = create_sink(sink_cfg['uri'], sink_cfg.get('params'))
    serializer = get_serializer(sink_cfg.get('format', DEFAULT_FORMAT))
    return Sink(sink_impl, serializer)


def _create_source(source_cfg):
    source_impl = create_source(source_cfg['uri'], source_cfg.get('params'))
    deserializer = get_deserializer(source_cfg.get('format', DEFAULT_FORMAT))
    return Source(source_impl, deserializer)


def _create_transform(transform_cfg):
    task_defs = transform_cfg.get('tasks', [])
    tasks = map(create_task, task_defs)
    return Transform(tasks, max_num_workers=transform_cfg.get('max_num_workers'))


class Engine(object):
    """
    The engine that orchestrates the end-to-end LandGrab job
    """
    def __init__(self, cfg):
        self.cfg = cfg

    def plan(self):
        """
        Builds out the plan for how to execute the job from the configuration contents
        """
        source = _create_source(self.cfg['source'])
        transform = _create_transform(self.cfg.get('transform', {}))
        sink = _create_sink(self.cfg['sink'])
        return source, transform, sink

    def run(self):
        """
        Actually runs the job in the following steps:
          1. Pulls the input source
          2. Applies any transformation tasks
          3. Saves the transformed data to the sink
        """
        source_uri = self.cfg['source']['uri']
        bag = dask.bytes.read_bytes(source_uri)
        print(bag.count().compute())


def run(cfg):
    engine = Engine(cfg)
    engine.run()
