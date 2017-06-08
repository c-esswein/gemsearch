from elasticsearch import Elasticsearch
from pprint import pprint

from gemsearch.core.item_iterator import ItemIterator
from gemsearch.storage.Storage import Storage

es = Elasticsearch()

def fill_db(limit):
    iterator = ItemIterator(limit)

    # TODO use typewriter not iterator
    
    for item in iterator.iterate([]):
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

#fill_db(500)
#clear()