from datetime import datetime
from elasticsearch import Elasticsearch
from graph_generator import GraphGenerator
from pprint import pprint
from Storage import Storage

es = Elasticsearch()

def fill_db(limit):
    generator = GraphGenerator('data/test2/')
    for item in generator.get_items(limit):
        if item['type'] == 'track-artist':
            doc = {
                'name': item['artistData']['name']
            }
            es.index(index="artist-index", doc_type='artist', id=item['artist'], body=doc)
        if item['type'] == 'playlist-track':
            doc = {
                'name': item['trackData']['name']
            }
            es.index(index="track-index", doc_type='track', id=item['track'], body=doc)
        if item['type'] == 'track-tag':
            doc = {
                'name': item['tagName']
            }
            es.index(index="tag-index", doc_type='tag', id=item['tag'], body=doc)

    es.indices.refresh(index="_all")

    print("data added")

def clear():
    es.indices.delete(index="artist-index")
    es.indices.delete(index="track-index")
    es.indices.delete(index="tag-index")
    print("all indexes cleared")

def search(queryStr):
        # "match_all": {}
    res = es.search(index="_all", body={"query": 
        #{"query_string":{"query":"machine gun","analyze_wildcard":True}}
        #{"match" : {"name" : "machina"}}
        {"match" : {"name" : {"query": queryStr, "fuzziness": "AUTO"}}}
        #{"match_phrase" : {"name" : "machine gun"}}
        #{"match_phrase": { "name": { "query": "machina gun", "slop": 3 } } }
    }) # , explain=True
    #print("Got %d Hits:" % res['hits']['total'])
    return [hit for hit in res['hits']['hits']]

def suggest():
    res = es.search(index="_all", body={
        "suggest": {
            "text" : "machina gun",
            "my-suggest-1" : {
                "term" : {
                    "field" : "name"
                }
            }
        }
    })
    #print("Got %d Hits:" % res['suggest']['total'])
    pprint(res['suggest'])

def extract_query_from_playlists():
    limit = 10
    playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(limit)

    for playlist in playlists:
        print(playlist['name'] + '______________')
        pprint(search(playlist['name']))

#fill_db(500)
#search()
#suggest()
#clear()
extract_query_from_playlists()