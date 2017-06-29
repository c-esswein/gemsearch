from gemsearch.storage.Storage import Storage

repos = Storage()

def resolve_items_meta(items):
    ''' Resolves metadata for all items in list.
    '''
    return [resolve_item_meta(item) for item in items]

def resolve_item_meta(item):
    ''' Resolves metadata for given item.
    '''

    if item['type'] == 'track':
        repoItem = repos.getCollection('tracks').find_one({'uri': item['id']})
        if repoItem:
            item['meta'] = copy_some(repoItem, ['preview_url', 'uri'])
            if 'album' in repoItem:
                item['meta']['images'] = repoItem['album']['images']

    if item['type'] == 'artist':
        repoItem = repos.getCollection('artists').find_one({'uri': item['id']})
        if repoItem:
            item['meta'] = copy_some(repoItem, ['uri', 'images'])

    return item


def copy_some(objfrom, names):
    objto = {}
    for n in names:
        if n in objfrom:
            objto[n] = objfrom[n]
    return objto


if __name__ == "__main__":
    from pprint import pprint
    pprint(resolve_items_meta([
        {
            "embeddingIndex": 19, 
            "id": "spotify:artist:1dNAH6pOWH5TQXhszDc8N3", 
            "name": "Contagious Love", 
            "type": "artist"
        }
    ]))
