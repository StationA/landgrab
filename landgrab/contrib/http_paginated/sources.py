import os
import tempfile
import requests
import jsonlines

from landgrab.source import BaseSource


APP_ID = os.environ['GENABILITY_APP_ID']
APP_KEY = os.environ['GENABILITY_APP_KEY']


def _process_uri(raw):
    return raw[len('http_paginated://'):]


def _sanitize(d):
    """
    Sanitizes strings
    """
    sanitized = {}
    for k, v in d.iteritems():
        if isinstance(v, dict):
            sanitized[k] = _sanitize(v)
        elif isinstance(v, list):
            sanitized[k] = [_sanitize(x) for x in v]
        elif isinstance(v, basestring):
            try:
                sanitized[k] = unicode(v.strip()).encode('ascii')
            except:
                sanitized[k] = None
    return sanitized


class HTTPPaginatedSource(BaseSource):
    """
    An input for paginated HTTP data that allows the page to be controlled through query params
    """
    def __init__(self, uri, page_count_param, page_count, page_index_param, max_pages,
                 current_page=0, status_check_name='not_provided', status_check_success_name=None,
                 query_params=None):
        self.uri = _process_uri(uri)
        self.page_count = page_count
        self.page_count_param = page_count_param
        self.page_index_param = page_index_param
        self.max_pages = max_pages
        self.current_page = current_page
        self.status_check_name = status_check_name
        self.status_check_success_name = status_check_success_name
        if query_params:
            self.query_params = query_params
        else:
            self.query_params = {}

    def __enter__(self):
        self.f = tempfile.NamedTemporaryFile(delete=True)
        with open(self.f.name, 'w') as tmpf:
            writer = jsonlines.Writer(tmpf)
            for query_params in self.query_param_generator():
                r = requests.get(self.uri, auth=(APP_ID, APP_KEY), params=query_params)
                if r.status_code < 400:
                    results = r.json()
                    if results.get(self.status_check_name) == self.status_check_success_name:
                        for tariff in results['results']:
                            tariff = _sanitize(tariff)
                            writer.write(tariff)
        return self

    def query_param_generator(self):
        page_index = 0
        for i in range(self.max_pages):
            query_params = {
                self.page_count_param: self.page_count,
                self.page_index_param: page_index
            }
            query_params.update(self.query_params)
            yield query_params
            page_index += self.page_count

    def pull(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()
