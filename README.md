# landgrab

[![pypi version](https://badge.fury.io/py/landgrab.svg)](https://badge.fury.io/py/landgrab)

Geospatial data hoarding system

## Installation

### Requirements

* Python 3.4+

### Install from PyPI (recommended)

```
pip install landgrab
```

### Installing from Github

```
pip install git+https://github.com/StationA/landgrab.git#egg=landgrab
```

### Installing from source

```
git clone https://github.com/StationA/landgrab.git
cd landgrab
pip install .
```

## Usage

```
Usage: landgrab [OPTIONS]

  Geospatial data hoarding system

Options:
  --version               Show the version and exit.
  -e, --env-file PATH
  -c, --config-file PATH  [required]
  -d, --debug
  -h, --help              Show this message and exit.
```

## Contributing

When contributing to this repository, please follow the steps below:

1. Fork the repository
1. Submit your patch in one commit, or a series of well-defined commits
1. Submit your pull request and make sure you reference the issue you are addressing

### Installing for development

```
pip install --editable .
```

### Running tests

```
tox -e dev
```
