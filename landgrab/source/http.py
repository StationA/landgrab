import codecs
import jsonlines
import requests
import tempfile
import urllib

from landgrab.source import BaseSource


class HTTPSource(BaseSource):
    """
    An input source for HTTP-based network data
    """
    def __init__(self, uri, method='GET', paginate=False, results_per_page_param=None,
                 results_per_page=None, page_index_param=None, max_pages=None, current_page=0,
                 query_params=None, results_key='results', username=None, password=None):
        self.uri = uri
        self.method = method
        self.paginate = paginate

        # Vars only necessary if paginate is `True`
        self.results_per_page = results_per_page
        self.results_per_page_param = results_per_page_param
        self.page_index_param = page_index_param
        self.max_pages = max_pages
        self.current_page = current_page
        if query_params:
            self.query_params = query_params
        else:
            self.query_params = {}
        self.results_key = results_key
        self.username = username
        self.password = password

    def __enter__(self):
        # TODO: Figure out if we can just use smart_open here instead
        # TODO: Figure out how to support different methods
        self.f = tempfile.NamedTemporaryFile(delete=True)
        if self.paginate:
            with codecs.open(self.f.name, mode='w', encoding='utf-8') as tmpf:
                writer = jsonlines.Writer(tmpf)
                for query_params in self._query_param_generator():
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
                    if r.status_code < 400:
                        results = r.json()
                        for tariff in results[self.results_key]:
                            writer.write(tariff)
        else:
            urllib.urlretrieve(self.uri, self.f.name)
        return self

    def _query_param_generator(self):
        page_index = self.current_page
        for i in range(self.max_pages):
            query_params = {
                self.results_per_page_param: self.results_per_page,
                self.page_index_param: page_index
            }
            query_params.update(self.query_params)
            yield query_params
            page_index += self.results_per_page

    def pull(self):
        return self.f

    def __exit__(self, *args):
        self.f.close()
        if not self.paginate:
            urllib.urlcleanup()
