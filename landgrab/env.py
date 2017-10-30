import os
import sys
import yaml

from landgrab.config import FORMATS, SOURCES, SINKS, TASKS


DEFAULT_PLUGIN_PATH = '~/.landgrab/plugins/'


def load(config_file):
    if not os.path.exists(config_file):
        return

    with open(config_file) as f:
        config = yaml.load(f)

    # Inject plugins to be used by job configurations
    plugins = config.get('plugins')
    sys.path.append(os.path.expanduser(DEFAULT_PLUGIN_PATH))
    for extra_path in plugins.get('python_path', []):
        sys.path.append(extra_path)
    if plugins.get('formats'):
        FORMATS.update(plugins['formats'])
    if plugins.get('sources'):
        SOURCES.update(plugins['sources'])
    if plugins.get('sinks'):
        SINKS.update(plugins['sinks'])
    if plugins.get('tasks'):
        TASKS.update(plugins['tasks'])
