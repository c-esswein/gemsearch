from pprint import pprint
from elasticsearch import Elasticsearch

es = Elasticsearch()

def search(queryStr):
        # "match_all": {}
    res = es.search(index="_all", body={"query": 
        {"match" : {"name" : {"query": queryStr, "fuzziness": "AUTO"}}}
        #{"match_phrase" : {"name" : "machine gun"}}
        #{"match_phrase": { "name": { "query": "machina gun", "slop": 3 } } }
    }) # , explain=True
    #print("Got %d Hits:" % res['hits']['total'])
    return [hit for hit in res['hits']['hits']]

def suggest(prefix):
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

def tester():
    from gemsearch.storage.Storage import Storage

    limit = 10
    playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(limit)

    for playlist in playlists:
        print(playlist['name'] + '______________')
        result = extract_query_from_name(playlist['name'])
        pprint(result)

def extract_query_from_name(name):
    hits = search(name)
    return [hit['_id'] for hit in hits][0:1]


if __name__ == '__main__':
    pprint(search('ni'))
    #suggest('ni')
