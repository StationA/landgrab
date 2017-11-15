from elasticsearch import Elasticsearch
from objectpath import Tree

from landgrab.sink import BaseSink


class ElasticSink(BaseSink):
    def __init__(self, uri, index, doc_type, doc_id_field):
        self.uri = uri[len('elastic://'):]
        self.index = index
        self.doc_type = doc_type
        self.doc_id_field = doc_id_field

    def __enter__(self):
        self.es = Elasticsearch(hosts=self.uri)
        return self

    def save(self, item):
        t = Tree(item)
        self.es.index(
            index=self.index,
            doc_type=self.doc_type,
            id=t.execute(self.doc_id_field),
            body=item
        )

    def __exit__(self, *args):
        pass
