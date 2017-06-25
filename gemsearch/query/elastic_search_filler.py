from elasticsearch import Elasticsearch
from pprint import pprint


class EsTypeWriter:
    '''Writes all entities into elastic search.
    '''

    def __init__(self):
        self.es = Elasticsearch()

    def addItem(self, idCounter, uidObj, type, name, obj = {}):
        doc = {
            'name': name
        }
        if 'uri' in obj:
            doc['uri'] = obj['uri']
            
        index = type+'-index'
        self.es.index(index=index, doc_type=type, id=uidObj, body=doc)

    def close_type_handler(self):
        self.es.indices.refresh(index='_all')

# ------------- static functions ------------

def clear():
    es = Elasticsearch()
    es.indices.delete(index='_all')
    print("all indexes cleared")


if __name__ == '__main__':
    # clear()
    pass
