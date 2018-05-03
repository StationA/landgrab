import ijson
import os
import shapefile
import shutil
import tempfile
import zipfile

from landgrab.format import BaseFormat


def _find_shp(d):
    for dirpath, _, files in os.walk(d):
        for f in files:
            fpath = os.path.join(dirpath, f)
            if f.endswith('.shp'):
                yield fpath


class GeoJSONFormat(BaseFormat):
    def deserialize(self, raw):
        """
        Deserializes from a raw input stream a new stream of GeoJSON Features
        """
        features = ijson.items(raw, 'features.item')
        for feature in features:
            yield feature

    def serialize(self, item):
        raise NotImplementedError


class ShapefileFormat(BaseFormat):
    def deserialize(self, raw):
        """
        Deserializes a raw stream of data from a ZIP archive containing shape files. The ZIP must at
        least include a .shp, .dbf, and .shx file to work using this format.

        The resulting output stream emits GeoJSON-style Feature dictionaries.
        """
        outfolder = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(raw) as zf:
                zf.extractall(outfolder)
            for shpfn in _find_shp(outfolder):
                shp = shapefile.Reader(shpfn)
                fields = [field[0] for field in shp.fields[1:]]
                for shape_record in shp.iterShapeRecords():
                    yield {
                        'geometry': shape_record.shape.__geo_interface__,
                        'properties': dict(zip(fields, shape_record.record))
                    }
        finally:
            shutil.rmtree(outfolder)

    def serialize(self, item):
        raise NotImplementedError
