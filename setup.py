#!/usr/bin/env python
from setuptools import setup, find_packages


def requirements(fn):
    with open(fn) as f:
        return f.read().splitlines()


setup(
    name='landgrab',
    version='0.1.15',
    description='Geospatial data hoarding system',
    author='Station A',
    author_email='software@stationa.com',
    url='https://github.com/StationA/landgrab',
    packages=find_packages(exclude=['*tests*']),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'landgrab=landgrab.__main__:main'
        ],
    },
    install_requires=requirements('./requirements.txt'),
    extras_require={
        'db': requirements('./requirements_db.txt'),
        'elastic': requirements('./requirements_elastic.txt'),
        'xls': requirements('./requirements_xls.txt'),
        'geo': requirements('./requirements_geo.txt')
    },
    tests_require=requirements('./test_requirements.txt'),
    license='License :: OSI Approved :: MIT License',
)
