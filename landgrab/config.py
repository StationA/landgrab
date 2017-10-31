from importlib import import_module
import os
import yaml


def import_class(class_path):
    mod, clazz = class_path.rsplit('.', 1)
    return getattr(import_module(mod), clazz)


DEFAULT_FORMAT = 'raw'
FORMATS = {
    'json': import_module('landgrab.format.json'),
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
}
SINKS = {
    'file': import_class('landgrab.sink.file.FileSink'),
    's3': import_class('landgrab.sink.s3.S3Sink'),
}


def _render(config_file):
    with open(config_file) as f:
        return os.path.expandvars(f.read())


# TODO: Implement configuration class
def load(config_file):
    config = _render(config_file)
    return yaml.load(config)


def get_deserializer(format):
    return FORMATS[format].deserialize


def get_serializer(format):
    return FORMATS[format].serialize


def create_source(uri, params=None):
    if ':' not in uri:
        uri = 'file://%s' % uri
    proto = uri.split(':')[0]
    ctor = SOURCES[proto]
    if params is None:
        params = {}
    return ctor(uri, **params)


def create_sink(uri, params):
    if ':' not in uri:
        uri = 'file://%s' % uri
    proto = uri.split(':')[0]
    ctor = SINKS[proto]
    if params is None:
        params = {}
    return ctor(uri, **params)


def create_task(task_def):
    ctor = TASKS[task_def['type']]
    kwargs = task_def.copy()
    del kwargs['type']
    return ctor(**kwargs)
