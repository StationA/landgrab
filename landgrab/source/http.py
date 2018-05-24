import json
import requests
import tempfile
import logging

from landgrab.source import BaseSource

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class HTTPSource(BaseSource):
    """
    An input source for HTTP-based network data
    """
    def __init__(self, uri, method='GET', query_params=None, results_key=None, username=None,
                 password=None, pagination=None):
        self.uri = uri
        self.method = method
        if pagination:
            self.paginate = True
            self.results_per_page = pagination.get('results_per_page', 25)
            self.results_per_page_param = pagination.get('results_per_page_param', None)
            self.page_offset_param = pagination.get('page_offset_param', None)
            self.max_pages = pagination.get('max_pages', 10)
            self.current_page = pagination.get('current_page', 0)
        else:
            self.paginate = False
        if query_params:
            self.query_params = query_params
        else:
            self.query_params = {}
        self.results_key = results_key
        self.username = username
        self.password = password

    def _make_request(self, query_params=None):
        if not query_params:
            query_params = self.query_params
        if self.username:
            r = requests.get(
                self.uri,
                auth=(self.username, self.password),
                params=query_params
            )
        else:
            r = requests.get(
                self.uri,
                params=query_params
            )
        return r

    def _pagination_query_param_generator(self):
        page_offset = self.current_page
        for i in range(self.max_pages):
            query_params = {
                self.results_per_page_param: self.results_per_page,
                self.page_offset_param: page_offset
            }
            query_params.update(self.query_params)
            yield query_params
            page_offset += self.results_per_page

    def __enter__(self):
        self.f = tempfile.NamedTemporaryFile(delete=True)
        with open(self.f.name, mode='wb') as tmpf:
            if self.paginate:
                for query_params in self._pagination_query_param_generator():
                    r = self._make_request(query_params)
                    if r.status_code < 400:
                        response = r.json()
                        if self.results_key:
                            results = response[self.results_key]
                        else:
                            results = response
                        if results:
                            for result in results:
                                tmpf.write(json.dumps(result))
                                tmpf.write('\n')
                        else:
                            LOGGER.debug('No results for: %s', r.url)
                            break
                    else:
                        LOGGER.debug('Error[%s] on HTTP request to: %s', (r.status_code, r.url))
                        break
            else:
                r = self._make_request()
                if r.status_code < 400:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            tmpf.write(chunk)
                else:
                    LOGGER.debug('Error[%s] on HTTP request to: %s', (r.status_code, r.url))
            return self

    def pull(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()
