from importlib import import_module
import os
import yaml


def import_class(class_path):
    mod, clazz = class_path.rsplit('.', 1)
    return getattr(import_module(mod), clazz)


DEFAULT_FORMAT = 'raw'
# TODO: Integrate these mappings into a more pluggable interface
FORMATS = {
    'jsonlines': import_module('landgrab.format.jsonlines'),
    'geojson': import_module('landgrab.format.geojson'),
    'raw': import_module('landgrab.format.raw'),
    'shp': import_module('landgrab.format.shp'),
}
SOURCES = {
    'http': import_class('landgrab.source.http.HTTPSource'),
    'https': import_class('landgrab.source.http.HTTPSource'),
    'file': import_class('landgrab.source.file.FileSource'),
    's3': import_class('landgrab.source.s3.S3Source'),
}
TASKS = {
    'extract': import_class('landgrab.transform.tasks.dict.ExtractTask'),
    'rename_key': import_class('landgrab.transform.tasks.dict.RenameKeyTask'),
    'project': import_class('landgrab.transform.tasks.dict.ProjectTask'),
    'buffer_geometry': import_class('landgrab.transform.tasks.geo.BufferGeometryTask'),
}
SINKS = {
    'file': import_class('landgrab.sink.file.FileSink'),
    's3': import_class('landgrab.sink.s3.S3Sink'),
}


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
    return FORMATS[format].deserialize


def get_serializer(format):
    """
    Gets the serialization function specified by the `format`
    """
    return FORMATS[format].serialize


def create_source(uri, params=None):
    """
    Constructs an input source from the URI spec and any additional source parameters. Note that
    when the URI does not have a scheme, the "file" scheme is assumed.
    """
    if ':' not in uri:
        uri = 'file://%s' % uri
    proto = uri.split(':')[0]
    ctor = SOURCES[proto]
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
    ctor = SINKS[proto]
    if params is None:
        params = {}
    return ctor(uri, **params)


def create_task(task_def):
    """
    Constructs a transformation task from the provided task definition
    """
    ctor = TASKS[task_def['type']]
    kwargs = task_def.copy()
    del kwargs['type']
    return ctor(**kwargs)
