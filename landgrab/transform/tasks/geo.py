from shapely.geometry import shape, mapping

from landgrab.transform import BaseTask


class BufferGeometryTask(BaseTask):
    """
    Buffers the geometry of a GeoJSON feature by a configurable buffer size amount, e.g.:

    - type: buffer_geometry
      buffer_size: 1

    This is useful when complex geometries have hard-to-detect inconsistencies in their coordinate
    rings, e.g. overlapping, closeness, etc.
    """
    def __init__(self, buffer_size=0):
        self.buffer_size = buffer_size

    def __call__(self, item):
        geom = item['geometry']
        s = shape(geom).buffer(self.buffer_size)
        buffered_geom = mapping(s)
        item['geometry'] = buffered_geom
        return item
