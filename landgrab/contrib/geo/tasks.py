from functools import partial
import json
from objectpath import Tree
import os
import pyproj
import requests
from shapely.geometry import shape, mapping
from shapely.ops import transform

from landgrab.task import BaseTask

PRESERVE_TOPOLOGY = False
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


def _google_geocode(address, google_api_key):
    url = ''.join([
        'https://maps.googleapis.com/maps/api/geocode/json?',
        'address=%s&' % address,
        'key=%s' % google_api_key
    ])
    res = requests.get(url)
    if res.status_code == 200:
        body = json.loads(res.text)
        location = body['results'][0]['geometry']['location']
        coords = [location['lng'], location['lat']]
        return coords


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
        try:
            s = shape(geom).buffer(self.buffer_size)
            if s.is_valid:
                buffered_geom = mapping(s)
                item['geometry'] = buffered_geom
                return item
        except IndexError:
            pass


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


class SimplifyGeometryTask(BaseTask):
    """
    Simplifies the geometry of a GeoJSON feature by a configurable tolerance amound, e.g.:

    - type: simplify_geometry
      tolerance: 0.05
      preserve_topology: False

    This is useful when complex geometries have unnecessary vertices that don't significantly alter
    their geometric representation. When `preserve_topology` is set to `False`, Shapely will use
    the much quicker Douglas-Peucker simplification algorithm.
    """
    def __init__(self, tolerance, preserve_topology=PRESERVE_TOPOLOGY):
        self.tolerance = tolerance
        self.preserve_topology = preserve_topology

    def __call__(self, item):
        geom = item['geometry']
        s = shape(geom).simplify(self.tolerance, self.preserve_topology)
        simplified_geom = mapping(s)
        item['geometry'] = simplified_geom
        return item


class GeocodeTask(BaseTask):
    """
    - type: geocode
      address: $.properties.address
      google_api_key: <GOOGLE_API_KEY>
    """
    def __init__(self, address, google_api_key=GOOGLE_API_KEY):
        self.address = address
        self.google_api_key = google_api_key

    def __call__(self, item):
        t = Tree(item)
        address = t.execute(self.address)
        coords = _google_geocode(address, self.google_api_key)
        try:
            if coords:
                item['geometry'] = {
                    'type': 'Point',
                    'coordinates': coords
                }
                return item
        except ValueError:
            pass
