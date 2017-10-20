from pprint import pprint
from elasticsearch.helpers import parallel_bulk
import os
from elasticsearch import Elasticsearch
from gemsearch.settings import GEMSEARCH_ELASTICSEARCH_HOST

def getEsInstance():
    dbHost = GEMSEARCH_ELASTICSEARCH_HOST
    es = Elasticsearch(
        [dbHost],
        http_auth=('elastic', 'changeme')
    )
    return es

def es_load_all_types(typeTraverser, indexName, docType, dismissTypes = []):
    es = getEsInstance()

    def esActionGenerator(traverser):
        ''' Transform type definitions into es documents.
        '''
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

    es.indices.refresh(index=indexName)
    pprint(es.count())

def es_reindex():
    es = getEsInstance()
    es.indices.refresh(index='_all')

def es_clear_indices():
    es = getEsInstance()
    es.indices.delete(index='_all')
    print("all indexes cleared")


if __name__ == '__main__':
    from gemsearch.core.data_loader import traverseTypes
    from gemsearch.utils.timer import Timer
    
    # es_clear_indices()
    with Timer(message='elastic search import') as t:
        es_load_all_types(traverseTypes('data/tmp/types.csv'), 'all_types', 'default_type')
    
