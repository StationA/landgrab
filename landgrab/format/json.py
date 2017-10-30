from __future__ import absolute_import
import json


def deserialize(raw):
    obj = json.loads(raw)
    return [obj]


def serialize(item):
    return json.dumps(item)
