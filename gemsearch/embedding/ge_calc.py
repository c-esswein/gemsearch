from pprint import pprint
import numpy as np
import csv
import scipy.spatial.distance

class GeCalc:
    '''Query embedded graph.
    '''

    def load_data(self, embeddingFile, typeFile):
        '''Loads embedding and type mapping.
        '''
        self.embedding = read_embedding_file(embeddingFile)
        self.lookup = read_type_file(typeFile)

    def load_node2vec_data(self, embeddingFile, typeFile):
        '''Loads embedding (stored in node2vec format) and type mapping.
        '''
        self.embedding = read_native_embedding_file(embeddingFile)
        self.lookup = read_type_file(typeFile)

    def get_item_info_by_index(self, index):
        '''Get item by embedding index.
        '''
        return self.lookup[index]

    def get_items_from_embedding_indices(self, indices, typeFilter = None):
        '''Maps embedding indices to items. Optional type Filter can be applied.
        '''
        result = []
        for itemIndex in indices:
            itemInfo = self.get_item_info_by_index(itemIndex)
            if (typeFilter is None) or (itemInfo['type'] in typeFilter):
                result.append(itemInfo)
        return result

    def get_item_by_item_id(self, itemId):
        '''Returns item info for obj id.
        '''
        for item in self.lookup:
            if item['id'] == itemId:
                return item
        return None

    def query_by_ids(self, ids, typeFilter = None, limit = 20):
        '''Query by obj ids.
        '''
        searchVec = None

        if len(ids) < 1:
            return []

        for id in ids:
            searchItem = self.get_item_by_item_id(id)
            if searchItem is None:
                raise ValueError('item id not found: ' + id)
            itemVec = self.embedding[searchItem['embeddingIndex']]
            
            if searchVec is not None:
                searchVec = searchVec + itemVec
            else:
                searchVec = itemVec

        result = find_similar_vecs(searchVec, self.embedding)
        result_items = self.get_items_from_embedding_indices(result, typeFilter)

        return result_items[:limit]

# ------------- static functions ------------

def read_type_file(file_name):
    '''Reads type file and creates lookup from embeddingIndex to items.
    '''
    lookup = []
    with open(file_name, 'r', encoding="utf-8") as csvfile:
        typeReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in typeReader:
            lookup.append({
                'embeddingIndex': int(row[0]),
                'id': row[1],
                'type': row[2],
                'name': row[3],
                'uri': row[4]
            })
    return lookup

def read_embedding_file(file_name):
    '''Load embedding.
    '''
    return np.loadtxt(file_name)


def read_native_embedding_file(file_name):
    ''' Load embedding stored by native node2vec
    '''
    with open(file_name, 'r') as f:
        n, d = f.readline().strip().split()
        X = np.zeros((int(n), int(d)))
        for line in f:
            emb = line.strip().split()
            emb_fl = [float(emb_i) for emb_i in emb[1:]]
            X[int(emb[0]), :] = emb_fl
    return X


def cos_cdist(matrix, vector):
    '''Compute the cosine distances between each row of matrix and vector.
    '''
    v = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, v, 'cosine').reshape(-1)

def find_similar_vecs(searchVec, vecs):
    '''Sorts vecs according to similarity to searchVec.
    '''
    simi = cos_cdist(vecs, searchVec)
    return np.argsort(simi)


if __name__ == '__main__':
    tmpDir = 'data/tmp_test/'
    ge = GeCalc()
    ge.load_data(tmpDir+'embedding.em', tmpDir+'types.csv')
    
    searchId = ['5730d5afa90a9a398dfb614c']

    print('Search for:\n')
    pprint(ge.get_item_by_item_id(searchId[0]))

    print('\nResults:\n')
    result_items = ge.query_by_ids(searchId, ['track'])
    for item in result_items:
        pprint(item)
    