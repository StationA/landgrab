from importlib import import_module
import os
import yaml


def import_class(class_path):
    mod, clazz = class_path.rsplit('.', 1)
    return getattr(import_module(mod), clazz)


DEFAULT_FORMAT = 'raw'
# TODO: Integrate these mappings into a more pluggable interface
FORMATS = {
    'jsonlines': 'landgrab.format.jsonlines.JSONLinesFormat',
    'raw': 'landgrab.format.raw.RawFormat',
    'rows': 'landgrab.format.rows.RowsFormat',
}
SOURCES = {
    'http': 'landgrab.source.http.HTTPSource',
    'https': 'landgrab.source.http.HTTPSource',
    'file': 'landgrab.source.file.FileSource',
    's3': 'landgrab.source.s3.S3Source',
}
TASKS = {
    'extract': 'landgrab.task.dict.ExtractTask',
    'rename_key': 'landgrab.task.dict.RenameKeyTask',
    'project': 'landgrab.task.dict.ProjectTask',
    'filter': 'landgrab.task.dict.FilterTask',
}
SINKS = {
    'file': 'landgrab.sink.file.FileSink',
    's3': 'landgrab.sink.s3.S3Sink',
}


class ConfigError(Exception):
    """
    Occurs when the job configuration is malformed or invalid
    """
    pass


def _render(config_file):
    """
    Expands shell-style environment variables found in the configuration file, e.g. `$USER`
    """
    with open(config_file) as f:
        return os.path.expandvars(f.read())


# TODO: Implement configuration class
def load(config_file):
    """
    Loads a configuration file into memory
    """
    config = _render(config_file)
    return yaml.load(config)


def get_deserializer(format):
    """
    Gets the deserialization function specified by the `format`
    """
    if format not in FORMATS:
        raise ConfigError('No such format: \'%s\'' % format)
    ctor = import_class(FORMATS[format])
    return ctor().deserialize


def get_serializer(format):
    """
    Gets the serialization function specified by the `format`
    """
    if format not in FORMATS:
        raise ConfigError('No such format: \'%s\'' % format)
    ctor = import_class(FORMATS[format])
    return ctor().serialize


def create_source(uri, params=None):
    """
    Constructs an input source from the URI spec and any additional source parameters. Note that
    when the URI does not have a scheme, the "file" scheme is assumed.
    """
    if ':' not in uri:
        uri = 'file://%s' % uri
    proto = uri.split(':')[0]
    if proto not in SOURCES:
        raise ConfigError('No such source: \'%s\'' % proto)
    ctor = import_class(SOURCES[proto])
    if params is None:
        params = {}
    return ctor(uri, **params)


def create_sink(uri, params):
    """
    Constructs an output sink from the URI spec and any additional sink parameters. Note that when
    the URI does not have a scheme, the "file" scheme is assumed.
    """
    if ':' not in uri:
        uri = 'file://%s' % uri
    proto = uri.split(':')[0]
    if proto not in SINKS:
        raise ConfigError('No such sink: \'%s\'' % proto)
    ctor = import_class(SINKS[proto])
    if params is None:
        params = {}
    return ctor(uri, **params)


def create_task(task_def):
    """
    Constructs a transformation task from the provided task definition
    """
    task_type = task_def['type']
    if task_type not in TASKS:
        raise ConfigError('No such task: \'%s\'' % task_type)
    ctor = import_class(TASKS[task_type])
    kwargs = task_def.copy()
    del kwargs['type']
    return ctor(**kwargs)
