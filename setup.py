#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession


SESSION = PipSession()


def requirements(fn):
    return [str(r.req) for r in parse_requirements(fn, session=SESSION)]

INSTALL_REQUIRES = requirements('./requirements.txt')
TESTS_REQUIRE = requirements('./test_requirements.txt')


setup(
    name='landgrab',
    version='0.1.0',
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
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'geo': requirements('landgrab/contrib/geo/requirements.txt')
    },
    tests_require=TESTS_REQUIRE,
    license='License :: Other/Proprietary License',
)
