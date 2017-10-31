from __future__ import absolute_import
import ijson


def deserialize(raw):
    features = ijson.items(raw, 'features.item')
    for feature in features:
        yield feature


def serialize(item):
    pass
