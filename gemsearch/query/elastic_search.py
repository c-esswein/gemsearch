from pprint import pprint
from elasticsearch import Elasticsearch
import os
import re

dbHost = os.environ.get('GEMSEARCH_ELASTICSEARCH_HOST', 'localhost')
es = Elasticsearch(
    [dbHost],
    http_auth=('elastic', 'changeme')
)

def search(queryStr, limit=10):
    res = es.search(index="_all", size=limit, body={
        "query": {"match" : {"name" : {"query": queryStr, "fuzziness": "AUTO"}}},
        "highlight" : {
            "fields" : {
                "name" : {}
            }
        },
        "explain": True
    })
    return [hit for hit in res['hits']['hits']]

def suggest(prefix, limit=10):
    return search(prefix, limit)

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
    })
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
    pprint(res)'''

def extract_query_from_name(name, limit=10):
    ''' Extract queryIds from given name. Uses simple search for name.
    '''
    hits = search(name, limit)
    return [hit['_source']['id'] for hit in hits]

def extract_multiple_queries_from_name(name, limit=1, resultIds = None):
    ''' Extracts queryIds from given name. Tries to extract more than one:
    Matches are analysed and removed from name, name is then used again as search query.
    '''
    highlightRegex = r"<em>([^<]*)</em>"
    subName = name

    if resultIds is None:
        resultIds = []

    results = search(name, limit)
    for resultItem in results:
        # add id to result arr
        resultIds.append(resultItem['_source']['id'])

        # remove matches from name
        matches = re.finditer(highlightRegex, resultItem['highlight']['name'][0])
        for match in matches:
            hit = match.group(1)
            # replace hit by empty string
            subName = re.compile(hit, re.IGNORECASE).sub('', subName).strip()

    # check if name has changed
    if name == subName:
        return resultIds

    # check if at least one alpha numeric char is left
    if not re.search('[a-zA-Z0-9]', subName):
        return resultIds        

    # continue extracting
    return extract_multiple_queries_from_name(subName, limit, resultIds)
