from landgrab.format import BaseFormat


class RowsFormat(BaseFormat):
    def deserialize(self, raw):
        """
        Deserializes from a raw input stream a new stream of dictionaries
        """
        for line in raw:
            yield dict(line)

    def serialize(self, item):
        raise NotImplementedError
