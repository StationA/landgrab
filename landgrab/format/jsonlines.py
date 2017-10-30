from __future__ import absolute_import
import json


def deserialize(raw):
    for line in raw.splitlines():
        yield json.loads(line)


def serialize(item):
    return json.dumps(item) + '\n'
