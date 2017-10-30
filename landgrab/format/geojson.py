from __future__ import absolute_import
import json


def deserialize(raw):
    obj = json.loads(raw)
    for feature in obj['features']:
        yield feature


def serialize(item):
    pass
