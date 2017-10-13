from pprint import pprint
from elasticsearch import Elasticsearch
import os

dbHost = os.environ.get('GEMSEARCH_ELASTICSEARCH_HOST', 'localhost')
es = Elasticsearch(
    [dbHost],
    http_auth=('elastic', 'changeme')
)

def search(queryStr, limit=10):
    res = es.search(index="_all", size=limit, body={"query": 
        {"match" : {"name" : {"query": queryStr, "fuzziness": "AUTO"}}}
    })
    return [hit for hit in res['hits']['hits']]

def suggest(prefix):
    # TODO: not used?
    '''res = es.search(index="_all", body={
        "suggest": {
            "name-suggest" : {
                "prefix" : prefix,
                "completion" : {
                    "field" : "name",
                    "fuzzy" : {
                        "fuzziness" : 2
                    }
                }
            }
        }
    })'''
    res = es.search(index="_all", body={
        "suggest": {
            "text" : "t",
            "my-suggest-1" : {
                "term" : {
                    "field" : "name"
                }
            }
        }
    })
    pprint(res)

def extract_query_from_name(name, limit=10):
    ''' Extract queryIds from given name. Uses simple search for name.
    '''
    hits = search(name, limit)
    return [hit['_source']['id'] for hit in hits]

def extract_all_possible_queries_from_name(name, limit=1):

    # TODO: split name into superset, query for all, append to result if not zero
    return extract_query_from_name(name, limit)
