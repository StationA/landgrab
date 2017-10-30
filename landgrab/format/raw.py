from landgrab.format import BaseFormat


class RawFormat(BaseFormat):
    def deserialize(self, raw):
        """
        Yields a new stream of the input data, untouched
        """
        for chunk in raw:
            yield chunk

    def serialize(self, item):
        """
        Identity function
        """
        return item
