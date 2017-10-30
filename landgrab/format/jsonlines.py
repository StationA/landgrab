import simplejson as json

from landgrab.format import BaseFormat


class JSONLinesFormat(BaseFormat):
    def deserialize(self, raw):
        """
        Deserializes from a raw input stream a new stream of JSON dictionaries
        """
        for line in raw:
            yield json.loads(line)

    def serialize(self, item):
        """
        Serializes each item as a JSON-encoded string with a line ending
        """
        return json.dumps(item) + '\n'
