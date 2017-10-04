from elasticsearch import Elasticsearch
from pprint import pprint
from elasticsearch.helpers import parallel_bulk
import os

dbHost = os.environ.get('GEMSEARCH_ELASTICSEARCH_HOST', 'localhost')

def es_get_instance():
    return Elasticsearch([dbHost])

def es_create_indices(index_name):
    # TODO: not implemented
    es = es_get_instance()
    es.indices.create(index=index_name, body=settings, ignore=404)

def es_load_all_types(typeTraverser, indexName, docType, dismissTypes = []):
    es = es_get_instance()

    def esActionGenerator(traverser):
        for typeDef in traverser:
            # check if item type should not be indexed
            if typeDef['type'] in dismissTypes:
                continue

            yield {
                '_op_type': 'index',
                '_index': indexName,
                '_type': docType,
                '_source': typeDef
            }

    for success, info in parallel_bulk(es, esActionGenerator(typeTraverser)):
        if not success: print('Doc failed', info)

    es.indices.refresh(index='_all')
    pprint(es.count())

def es_reindex():
    es = es_get_instance()
    es.indices.refresh(index='_all')

def es_clear_indices():
    es = es_get_instance()
    es.indices.delete(index='_all')
    print("all indexes cleared")


if __name__ == '__main__':
    from gemsearch.core.data_loader import traverseTypes
    from gemsearch.utils.timer import Timer
    
    # es_clear_indices()
    with Timer(message='elastic search import') as t:
        es_load_all_types(traverseTypes('data/tmp/types.csv'), 'all_types', 'default_type')
    
