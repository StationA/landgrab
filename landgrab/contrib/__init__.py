from landgrab.config import FORMATS, TASKS


def load():
    FORMATS['geojson'] = 'landgrab.contrib.geo.formats.GeoJSONFormat'
    FORMATS['shp'] = 'landgrab.contrib.geo.formats.ShapefileFormat'
    TASKS['buffer_geometry'] = 'landgrab.contrib.geo.tasks.BufferGeometryTask'
    TASKS['project_geometry'] = 'landgrab.contrib.geo.tasks.ProjectGeometryTask'
