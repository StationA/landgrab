from __future__ import absolute_import
import ijson


def deserialize(raw):
    """
    Deserializes from a raw input stream a new stream of GeoJSON Features
    """
    features = ijson.items(raw, 'features.item')
    for feature in features:
        yield feature


def serialize(item):
    raise NotImplementedError
