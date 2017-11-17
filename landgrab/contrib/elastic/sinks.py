from elasticsearch import helpers, Elasticsearch
from objectpath import Tree

from landgrab.sink import BaseSink


def _generate_docs(docs, index, doc_type, doc_id_field):
    for doc in docs:
        t = Tree(doc)
        yield {
            '_index': index,
            '_type': doc_type,
            '_id': t.execute(doc_id_field),
            '_source': doc
        }


class ElasticSink(BaseSink):
    def __init__(self, uri, index, doc_type, doc_id_field, chunk_size=500):
        self.uri = uri[len('elastic://'):]
        self.index = index
        self.doc_type = doc_type
        self.doc_id_field = doc_id_field
        self.chunk_size = chunk_size

    def __enter__(self):
        self.es = Elasticsearch(hosts=self.uri, timeout=300)
        return self

    def save_stream(self, items):
        docs = _generate_docs(items, self.index, self.doc_type, self.doc_id_field)
        helpers.bulk(self.es, docs, chunk_size=self.chunk_size, refresh=True)

    def __exit__(self, *args):
        pass
