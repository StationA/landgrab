from functools import partial
import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform

from landgrab.task import BaseTask


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


class ProjectGeometryTask(BaseTask):
    """
    Projects the geometry of a GeoJSON feature to a configurable spatial reference system, e.g.:

    - type: project_geometry
      in_system: EPSG:26986
      out_system: EPSG:4326
    """
    def __init__(self, in_system, out_system):
        self.in_system = in_system
        self.out_system = out_system

    def __call__(self, item):
        geom = item['geometry']
        project = partial(
            pyproj.transform,
            pyproj.Proj(init=self.in_system),
            pyproj.Proj(init=self.out_system, preserve_units=True)
        )
        s = transform(
            project,
            shape(geom)
        )
        projected_geom = mapping(s)
        item['geometry'] = projected_geom
        return item
