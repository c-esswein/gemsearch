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

def find_similar_vecs(item, data):
    simi = cos_cdist(data, item)
    return np.argsort(simi)





class GeCalc:

    def __init__(self, storage_prefix):
        self.load_data(storage_prefix)

    def load_data(self, prefix):
        embeddingLbl, embedding = read_v_file(prefix + 'test.adj')
        lookup = read_type_file(prefix + 'types-all.csv')

        self.embeddingLbl = embeddingLbl
        self.embedding = embedding
        self.lookup = lookup

    def get_item_info(self, label):
        return self.lookup[str(label)]

    def get_items_from_embedding_indices(self, items, typeFilter = None):
        result = []
        for itemIndex in items:
            itemInfo = self.get_item_info(self.embeddingLbl[itemIndex])
            if (typeFilter is None) or (itemInfo['type'] in typeFilter):
                result.append(itemInfo)
        return result

    def get_item_by_item_id(self, itemId):
        for lblKey in self.lookup:
            if self.lookup[lblKey]['id'] == itemId:
                return self.lookup[lblKey]
        return None

    def query_by_ids(self, ids, typeFilter = None):
        searchVec = None

        if len(ids) < 1:
            return []

        for id in ids:
            searchItem = self.get_item_by_item_id(id)
            searchLbl = searchItem['embeddingKey']
            try:
                searchIndex = self.embeddingLbl.index(int(searchLbl))
            except ValueError:
                pprint('search item not in graph')
                raise ValueError
            
            if searchVec is not None:
                searchVec = searchVec + self.embedding[searchIndex]
                pprint(self.embedding[searchIndex])
            else:
                searchVec = self.embedding[searchIndex]


        result = find_similar_vecs(searchVec, self.embedding)
        result_items = self.get_items_from_embedding_indices(result, typeFilter)

        return result_items

if __name__ == '__main__':
    ge = GeCalc('graph-embedding/')

    searchId = '5730d9b5a90a9a398dff540b'

    print('Search for:\n')
    pprint(ge.get_item_by_item_id(searchId))

    print('\nResults:\n')
    result_items = ge.query_by_ids(searchId)
    for item in result_items:
        pprint(item)
