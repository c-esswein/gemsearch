import unittest

from gemsearch.embedding.ge_calc import GeCalc


dataDir = 'data/test_data/'

class GeCalcTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.geCalc = GeCalc()
        cls.geCalc.load_node2vec_data(dataDir+'node2vec.em', dataDir+'types.csv')


    def test_VecQuery(self):
        geCalc = self.geCalc
        for i in range(0, len(geCalc.embedding) -1):
            searchVec = geCalc.embedding[i]

            queryRes = geCalc.query_by_vec(searchVec, limit = 1)
            self.assertEqual(queryRes[0]['embeddingIndex'], i)

    def test_IdQuery(self):
        geCalc = self.geCalc
        for i in range(0, len(geCalc.lookup) -1):
            searchId = geCalc.lookup[i]['id']

            queryRes = geCalc.query_by_ids([searchId], limit = 1)
            self.assertEqual(queryRes[0]['id'], searchId)


    def test_TypeFilter(self):
        geCalc = self.geCalc
        typeFilter = ['track']
        limit = 30
        
        for i in range(0, len(geCalc.lookup) -1):
            searchId = geCalc.lookup[i]['id']

            queryRes = geCalc.query_by_ids([searchId], typeFilter, limit)
            for res in queryRes:
                self.assertIn(res['type'], typeFilter)


if __name__ == '__main__':
    unittest.main()
