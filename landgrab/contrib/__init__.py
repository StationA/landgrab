from landgrab.config import FORMATS, SINKS, SOURCES, TASKS


def load():
    FORMATS['geojson'] = 'landgrab.contrib.geo.formats.GeoJSONFormat'
    FORMATS['shp'] = 'landgrab.contrib.geo.formats.ShapefileFormat'
    FORMATS['xls'] = 'landgrab.contrib.xls.formats.XLSFormat'
    FORMATS['csv'] = 'landgrab.contrib.xls.formats.XLSFormat'
    FORMATS['xlsx'] = 'landgrab.contrib.xls.formats.XLSFormat'
    SINKS['elastic'] = 'landgrab.contrib.elastic.sinks.ElasticSink'
    SOURCES['sql'] = 'landgrab.contrib.db.sources.SQLSource'
    TASKS['buffer_geometry'] = 'landgrab.contrib.geo.tasks.BufferGeometryTask'
    TASKS['project_geometry'] = 'landgrab.contrib.geo.tasks.ProjectGeometryTask'
    TASKS['simplify_geometry'] = 'landgrab.contrib.geo.tasks.SimplifyGeometryTask'
    TASKS['geocode'] = 'landgrab.contrib.geo.tasks.GeocodeTask'
