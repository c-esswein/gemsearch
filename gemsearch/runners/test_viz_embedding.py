''' Compare results of 3D reduced embedding.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
from gemsearch.embedding.ge_calc import GeCalc
import numpy as np
from pprint import pprint

dataDir = 'data/test_data/'



fullModelCalc = GeCalc()
fullModelCalc.load_node2vec_data(dataDir+'node2vec.em', dataDir+'types.csv')

vizModelCalc = GeCalc()
vizModelCalc.load_lookup(dataDir+'types.csv')
vizModelCalc.embedding = np.load(dataDir+'pca.em.npy')

if len(vizModelCalc.embedding) != len(vizModelCalc.lookup):
    raise Exception('Embeddings ({}) and type-mappings ({}) size does not match for viz embedding'.format(len(vizModelCalc.embedding), len(vizModelCalc.lookup)))

def checkMatches(recResult, testTracks):
    hits = 0
    for track in testTracks:
        if track in recResult:
            hits += 1

    return hits


def testPrecisionById():
    typeFilter = ['track']
    modelSize = len(fullModelCalc.lookup)
    limit = 30
    precision = 0

    for i in range(0, modelSize - 1):
        # query by item
        searchId = fullModelCalc.lookup[i]['id']
        searchIdViz = vizModelCalc.lookup[i]['id']

        if not (searchId == searchIdViz):
            raise Exception('ids are not equal')

        fullModelRes = [item['id'] for item in fullModelCalc.query_by_ids([searchId], typeFilter, limit)]
        vizModelRes = [item['id'] for item in vizModelCalc.query_by_ids([searchId], typeFilter, limit)]

        # check limit
        if len(fullModelRes) < limit or not (len(fullModelRes) == len(vizModelRes)):
            raise Exception('invalid return sizes')

        # compare results
        hits = checkMatches(vizModelRes, fullModelRes)
        precision = hits / limit

    precision /= modelSize
    print('total precision: ' + str(precision))

testPrecisionById()


print('done')