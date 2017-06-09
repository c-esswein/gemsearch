from pprint import pprint
import numpy as np
import csv
import scipy.spatial.distance

class GeCalc:
    '''Query embedded graph.
    '''

    def __init__(self, storage_prefix):
        self.load_data(storage_prefix)

    def load_data(self, prefix):
        '''Loads embedding and type mapping.
        '''
        self.prefix = prefix
        embeddingLbl, embedding = read_v_file(prefix + 'embedding.adj')
        lookup = read_type_file(prefix + 'types.csv')

        self.embeddingLbl = embeddingLbl
        self.embedding = embedding
        self.lookup = lookup

    def get_item_info(self, label):
        '''Get item by label id.
        '''
        return self.lookup[str(label)]

    def get_items_from_embedding_indices(self, items, typeFilter = None):
        '''Maps embedding indices to items. Optional type Filter can be applied.
        '''
        result = []
        for itemIndex in items:
            itemInfo = self.get_item_info(self.embeddingLbl[itemIndex])
            if (typeFilter is None) or (itemInfo['type'] in typeFilter):
                result.append(itemInfo)
        return result

    def get_item_by_item_id(self, itemId):
        '''Returns item info for obj id.
        '''
        for lblKey in self.lookup:
            if self.lookup[lblKey]['id'] == itemId:
                return self.lookup[lblKey]
        return None

    def query_by_ids(self, ids, typeFilter = None, limit = 20):
        '''Query by obj ids.
        '''
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

        return result_items[:limit]

    def get_graph_data(self):
        '''Get 3D graph coordinates for all items.
        '''
        # todo real 3d vecs
        return self.embedding[:,0:3].flatten()

    def get_lbl_mapping(self):
        '''Returns mapping from lables to items.
        '''
        return list(map(lambda lbl: self.get_item_info(lbl), self.embeddingLbl))

    def get_graph(self):
        '''Get edge list. Node IDs are embedding indices.
        '''
        nodes = read_graph_file(self.prefix + 'graph.txt')

        # transform lables into indices of embedding
        def get_i(lbl):
            return self.embeddingLbl.index(lbl)
        arr = list(map(lambda lbls: [get_i(lbls[0]), get_i(lbls[1])], nodes))
        return np.array(arr).flatten()

    def clean_graph(self):
        '''Removes all unused entries in graph. Only usefull if not fully connected
        graph is used.
        '''
        graph = self.get_graph()
        pprint(len(graph))

        with open(self.prefix + 'graph-cleaned.txt', 'w') as outfile:
            for pair in graph:
                if pair[0] in self.embeddingLbl and pair[1] in self.embeddingLbl:
                    outfile.write(str(pair[0])+' '+str(pair[1]) + '\n')

        return "removed unused entries"


# ------------- static functions ------------

def read_type_file(file_name):
    '''Reads type file and creates lookup from embeddingKey to items.
    '''
    lookup = {}
    with open(file_name, 'r', encoding="utf-8") as csvfile:
        typeReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in typeReader:
            lookup[row[0]] = {
                'embeddingKey': row[0],
                'type': row[1],
                'id': row[2],
                'name': row[3],
                'uri': row[4]
            }
    return lookup

def read_v_file(file_name):
    '''Load embedding.
    '''
    embeddingLbl = []
    points = []
    with open(file_name, 'r') as f:
        f.readline() # Discard the number of edges
        for line in f:
            edge = line.strip().split()
            embeddingLbl.append(int(edge[0]))
            pointV = []
            for v in edge[1:]:
                pointV.append(float(v))
            points.append(pointV)
    return embeddingLbl, np.array(points)


def read_graph_file(file_name):
    '''Load Graph.
    '''
    connections = []
    with open(file_name, 'r') as f:
        for line in f:
            edge = line.strip().split()
            pointV = []
            for v in edge:
                pointV.append(int(v))
            connections.append(pointV)
    return connections


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
    ge = GeCalc('data/tmp_test/')
    
    searchId = ['5730d9b5a90a9a398dff540b']

    print('Search for:\n')
    pprint(ge.get_item_by_item_id(searchId))

    print('\nResults:\n')
    result_items = ge.query_by_ids(searchId, ['track'])
    for item in result_items:
        pprint(item)
    

    #pprint(ge.get_graph())
    #pprint(ge.clean_graph())
