# -*- coding: utf-8 -*-
import os.path
import click

import landgrab
import landgrab.config as config
import landgrab.contrib as contrib
import landgrab.engine as engine
import landgrab.env as env


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CWD = os.path.abspath(os.getcwd())


@click.command('landgrab', short_help='Geospatial data hoarding system',
               context_settings=CONTEXT_SETTINGS)
@click.version_option(version=landgrab.__version__, prog_name='landgrab')
@click.option('--env-file', '-e', type=click.Path(exists=False, dir_okay=False,
                                                  readable=True, resolve_path=True),
              default=os.path.expanduser('~/.landgrab/config.yaml'))
@click.option('--config-file', '-c', type=click.Path(exists=True, dir_okay=False, readable=True,
                                                     resolve_path=True), required=True)
@click.option('--debug', '-d', is_flag=True)
def run(env_file, config_file, debug):
    """Geospatial data hoarding system
    """
    env.load(env_file)
    contrib.load()
    cfg = config.load(config_file)
    engine.run(cfg)


def main():
    run()


if __name__ == '__main__':
    main()
