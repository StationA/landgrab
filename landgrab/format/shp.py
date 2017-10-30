import os
import shapefile
import tempfile
import zipfile
from StringIO import StringIO


def _find_shp(d):
    for dirpath, _, files in os.walk(d):
        for f in files:
            fpath = os.path.join(dirpath, f)
            if f.endswith('.shp'):
                return fpath
    raise IOError('No .shp file found in directory %s' % d)


def deserialize(raw):
    outfolder = tempfile.mkdtemp()
    buf = StringIO(raw)
    with zipfile.ZipFile(buf) as zf:
        zf.extractall(outfolder)
    shpfn = _find_shp(outfolder)
    shp = shapefile.Reader(shpfn)
    fields = [field[0] for field in shp.fields[1:]]
    for shape_record in shp.iterShapeRecords():
        yield {
            'geometry': shape_record.shape.__geo_interface__,
            'properties': dict(zip(fields, shape_record.record))
        }
