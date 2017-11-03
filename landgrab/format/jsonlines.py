from __future__ import absolute_import
import simplejson as json


def deserialize(raw):
    """
    Deserializes from a raw input stream a new stream of JSON dictionaries
    """
    for line in raw:
        yield json.loads(line)


def serialize(item):
    """
    Serializes each item as a JSON-encoded string with a line ending
    """
    return json.dumps(item)
