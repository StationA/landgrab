# -*- coding: utf-8 -*-
import os.path
import click

import landgrab

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CWD = os.path.abspath(os.getcwd())


@click.command('landgrab', short_help='Geospatial data hoarding system',
               context_settings=CONTEXT_SETTINGS)
@click.version_option(version=landgrab.__version__,
                      prog_name='landgrab')
def run():
    """Geospatial data hoarding system
    """
    print('Welcome to my awesome program!')


def main():
    run()


if __name__ == '__main__':
    main()
