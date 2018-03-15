import simplejson
import pandas as pd

from landgrab.format import BaseFormat


class XLSFormat(BaseFormat):
    def deserialize(self, raw):
        """
        Deserializes from a raw input stream a new stream of XLS rows
        """
        df = pd.read_excel(raw)
        for row in simplejson.loads(df.to_json(orient='records')):
            yield row

    def serialize(self, item):
        raise NotImplementedError
