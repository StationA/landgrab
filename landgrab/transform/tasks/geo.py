from shapely.geometry import shape, mapping

from landgrab.transform import BaseTask


class BufferGeometryTask(BaseTask):
    def __init__(self, buffer_size=0):
        self.buffer_size = buffer_size

    def __call__(self, item):
        """
        Given a GeoJSON Feature, buffers the geometry
        """
        geom = item['geometry']
        s = shape(geom).buffer(0)
        buffered_geom = mapping(s)
        item['geometry'] = buffered_geom
        return item
