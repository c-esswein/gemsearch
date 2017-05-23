from pprint import pprint
import numpy as np
import csv
import scipy.spatial.distance

def read_type_file(file_name):
    lookup = {}
    with open(file_name, 'r', encoding="utf-8") as csvfile:
        typeReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in typeReader:
            lookup[row[0]] = {
                'embeddingKey': row[0],
                'type': row[1],
                'id': row[2],
                'name': row[3]
            }
    return lookup

def read_v_file(file_name):
    embeddingLbl = []
    points = []
    with open(file_name, 'r') as f:
        f.readline() # Discard the number of edges
        for line in f:
            edge = line.strip().split()
            embeddingLbl.append(int(edge[0]))
            pointV = []
            for v in edge[0:]:
                pointV.append(float(v))
            points.append(pointV)
    return embeddingLbl, np.array(points)

def cos_cdist(matrix, vector):
    """
    Compute the cosine distances between each row of matrix and vector.
    """
    v = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, v, 'cosine').reshape(-1)

def get_item_info(label, lookup):
    return lookup[str(label)]


def find_similar_vecs(item, data):
    simi = cos_cdist(data, item)
    return np.argsort(simi)

def get_items_from_embedding_indices(items, lookup, embeddingLbl, typeFilter = None):
    result = []
    for itemIndex in items:
        itemInfo = get_item_info(embeddingLbl[itemIndex], lookup)
        if (typeFilter is None) or (itemInfo['type'] in typeFilter):
            result.append(itemInfo)
    return result

def get_item_by_item_id(lookup, itemId):
    for lblKey in lookup:
        if lookup[lblKey]['id'] == itemId:
            return lookup[lblKey]
    return None

#### MAIN ####
def main():
    embeddingLbl, embedding = read_v_file('graph-embedding/test.adj')
    lookup = read_type_file('graph-embedding/types-all.csv')

    searchItem = get_item_by_item_id(lookup, '5730d9b5a90a9a398dff540b')
    searchLbl = searchItem['embeddingKey']
    try:
        searchIndex = embeddingLbl.index(int(searchLbl))
    except ValueError:
        pprint('search item not in graph')
        return

    searchVec = embedding[searchIndex]

    print('Search for:\n')
    pprint(get_item_info(searchLbl, lookup))

    print('\n\nResults:\n')
    result = find_similar_vecs(searchVec, embedding)
    result_items = get_items_from_embedding_indices(result, lookup, embeddingLbl) #, ['track', 'artist']
    for item in result_items:
        pprint(item)

main()