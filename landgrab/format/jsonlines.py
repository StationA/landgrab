from __future__ import absolute_import
import simplejson as json


def deserialize(raw):
    for line in raw:
        yield json.loads(line)


def serialize(item):
    return json.dumps(item) + '\n'
