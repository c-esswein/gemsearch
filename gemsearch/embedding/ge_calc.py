import numpy as np
import csv
import random
import sys
import scipy.spatial.distance
from gemsearch.core.data_loader import traverseTypes

class GeCalc:
    '''Class to load and query embeddings.
    '''

    embedding = None    # embeddings array
    lookup = None       # type lookup, maps embedding key to type data

    def load_lookup(self, typeFile):
        '''Loads type mapping.
        '''

        self.lookup = list(traverseTypes(typeFile))

    def load_node2vec_data(self, embeddingFile, typeFile):
        '''Loads embedding (stored in node2vec format) and type mapping.
        '''
        self.embedding = read_native_embedding_file(embeddingFile)
        self.load_lookup(typeFile)

        if len(self.embedding) != len(self.lookup):
            raise Exception('Embeddings ({}) and type-mappings ({}) size does not match'.format(len(self.embedding), len(self.lookup)))

    def get_item_info_by_index(self, index):
        '''Get item by embedding index.
        '''
        return self.lookup[index]

    def get_items_from_embedding_indices(self, indices, typeFilter = None, limit = sys.maxsize, offset = 0, skipIds = []):
        '''Maps embedding indices to items. Optional type Filter can be applied. Items are skiped if id is in skipIds.
        '''
        result = []
        found = 0
        for itemIndex in indices:
            itemInfo = self.get_item_info_by_index(itemIndex)

            # filter type based on typeFilter
            if (typeFilter is not None) and (itemInfo['type'] not in typeFilter):
                continue

            # check if item should be skiped
            if itemInfo['id'] in skipIds:
                continue

            # check offset
            if offset > 0:
                offset -= 1
                continue

            # valid item
            result.append(itemInfo)
            found += 1
            if found == limit:
                break

        return result

    def get_item_by_item_id(self, itemId):
        '''Returns item info for obj id.
        '''
        for item in self.lookup:
            if item['id'] == itemId:
                return item
        return None

    def get_embedding_for_id(self, id):
        ''' Returns embedding vector of given id.
        '''
        searchItem = self.get_item_by_item_id(id)
        if searchItem is None:
            raise ValueError('item id not found: ' + id)
        itemVec = self.embedding[searchItem['embeddingIndex']]

        return itemVec

    def query_by_ids(self, ids, typeFilter = None, limit = 20, offset = 0, skipIds = []):
        '''Query by obj ids.
        '''
        searchVec = None

        if len(ids) < 1:
            return []

        for id in ids:
            itemVec = self.get_embedding_for_id(id)

            if searchVec is not None:
                searchVec = searchVec + itemVec
            else:
                searchVec = itemVec

        return self.query_by_vec(searchVec, typeFilter, limit, offset, skipIds)

    def query_by_vec(self, searchVec, typeFilter = None, limit = 20, offset = 0, skipIds = []):
        ''' Query by embeddings searchVec
        '''
        result = find_similar_vecs(searchVec, self.embedding)
        result_items = self.get_items_from_embedding_indices(result, typeFilter, limit, offset, skipIds)

        return result_items

    def random_query_results(self, typeFilter = None, limit = 20):
        '''Returns random entries with given optional typeFilter
        '''
        maxIndex = len(self.lookup)
        result = []

        while len(result) < limit:
            randomIndex = random.randint(0, maxIndex - 1)
            itemInfo = self.get_item_info_by_index(randomIndex)
            if (typeFilter is None) or (itemInfo['type'] in typeFilter):
                result.append(itemInfo)

        return result


    def get_distance(self, nodeAId, nodeBId):
        '''Returns distance between two nodes.
        '''
        return scipy.spatial.distance.cosine(self.embedding[nodeAId], self.embedding[nodeBId])

    def get_graph_embedding(self, typeFilter = None):
        '''Get 3D graph coordinates for all items.
        '''
        # todo typeFilter
        # todo real 3d vecs
        return self.embedding[:,0:3].flatten()

    def get_lookup(self):
        #TODO: still used by api?
        return self.lookup

# ------------- static functions ------------

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
    return scipy.spatial.distance.cdist(matrix, v, 'euclidean').reshape(-1)


def find_similar_vecs(searchVec, vecs):
    '''Sorts vecs according to similarity to searchVec.
    '''
    simi = cos_cdist(vecs, searchVec)
    return np.argsort(simi)


if __name__ == '__main__':
    from gemsearch.utils.timer import Timer
    from pprint import pprint

    testVecs = np.array([[1,1,1], [1, 2, 3], [1, 2, 4], [1, 3, 3], [2, 2, 3], [5,5,5], [8,8,8], [9,2,4]])
    searchVec = np.array([1,1,1])

    res = cos_cdist(testVecs, searchVec)
    # np.absolute(
    pprint(res)
    sortedI = np.argsort(res)
    pprint(sortedI)
    pprint(list(testVecs[i] for i in sortedI))

    ''' tmpDir = 'data/tmp/'
    ge = GeCalc()
    
    with Timer(message='Data loading') as t:
        ge.load_node2vec_data(tmpDir+'node2vec.em', tmpDir+'types.csv')
    
    searchId = ['tag::club house']

    print('Search for:\n')
    pprint(ge.get_item_by_item_id(searchId[0]))

    print('\nResults:\n')
    with Timer(message='Query') as t:
        result_items = ge.query_by_ids(searchId, ['track'], 10) '''
