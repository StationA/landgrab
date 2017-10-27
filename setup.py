#!/usr/bin/env python
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession


SESSION = PipSession()
INSTALL_REQUIRES = [str(r.req) for r in
                    parse_requirements('./requirements.txt', session=SESSION)]
TESTS_REQUIRE = [str(r.req) for r in
                 parse_requirements('./test_requirements.txt', session=SESSION)]


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
    tests_require=TESTS_REQUIRE,
    license='License :: Other/Proprietary License',
)
