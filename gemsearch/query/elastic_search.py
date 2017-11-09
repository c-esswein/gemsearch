from pprint import pprint
import os
import re
from elasticsearch import Elasticsearch
from gemsearch.settings import GEMSEARCH_ELASTICSEARCH_HOST

dbHost = GEMSEARCH_ELASTICSEARCH_HOST
es = Elasticsearch(
    [dbHost],
    http_auth=('elastic', 'changeme')
)

def search(queryStr, limit=10, itemType = None):
    query = {"match" :{"name" : {"query": queryStr, "fuzziness": "AUTO"}}}

    if itemType is not None:
        query = {"bool": {"must": [{"match": {"type": itemType}}, query]}}

    res = es.search(index="_all", size=limit, body={
        "query": query,
        "highlight" : {
            "fields" : {
                "name" : {}
            }
        }
    })
    return [hit for hit in res['hits']['hits']]




def suggest(prefix, limit=10, itemType = None):
    ''' Get autocomplete suggestions for given prefix. If prefix starts with "#" return item types
    are limited to tags when itemType is not set.
    '''
    if itemType is None and prefix.startswith('#'):
        itemType = 'tag'
        prefix = prefix[1:]

    return search(prefix, limit, itemType)

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

if __name__ == '__main__':
    from pprint import pprint
    pprint(suggest('#test'))
