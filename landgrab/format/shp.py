import os
import shapefile
import shutil
import tempfile
import zipfile


def _find_shp(d):
    for dirpath, _, files in os.walk(d):
        for f in files:
            fpath = os.path.join(dirpath, f)
            if f.endswith('.shp'):
                return fpath
    raise IOError('No .shp file found in directory %s' % d)


def deserialize(raw):
    outfolder = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(raw) as zf:
            zf.extractall(outfolder)
        shpfn = _find_shp(outfolder)
        shp = shapefile.Reader(shpfn)
        fields = [field[0] for field in shp.fields[1:]]
        for shape_record in shp.iterShapeRecords():
            yield {
                'geometry': shape_record.shape.__geo_interface__,
                'properties': dict(zip(fields, shape_record.record))
            }
    finally:
        shutil.rmtree(outfolder)
