import unittest

from gemsearch.api.positions import cluster_items
from pprint import pprint

class ClusterTest(unittest.TestCase):

    def test_bounding_box(self):
        items = [
            {'position': [0, 0, 0]},
            {'position': [-1, 2, 4]},
            {'position': [-9, -2, 4]},
            {'position': [8, 2, 4]},
            {'position': [3, 2, 7]},
            {'position': [-1, -7, 14]}
        ]

        cluster, boundingBox = cluster_items(items, 2)

        self.assertEqual(boundingBox[0].tolist(), [-9, -7, 0])
        self.assertEqual(boundingBox[1].tolist(), [8, 2, 14])

    def test_small_bounding_box(self):
        print('here')
        items = [
            {'position': [0, 0, 0]},            
            {'position': [-0.04607822019814664, 0.01028123260686703, -0.009728830190129899]},
            {'position': [0.016531214731048155, -0.031884937470645025, 0.03467921747132994]},
        ]

        cluster, boundingBox = cluster_items(items, 2)

        self.assertEqual(boundingBox[0].tolist(), [-0.04607822019814664, -0.031884937470645025, -0.009728830190129899])
        self.assertEqual(boundingBox[1].tolist(), [0.016531214731048155, 0.01028123260686703, 0.03467921747132994])

    def test_cluster(self):
        items = [
            {'position': [0, 0, 0]},
            {'position': [1, 1, 1]},
            {'position': [10, 10, 10]},
            {'position': [11, 11, 11]},
            {'position': [20, 20, 22]},
            {'position': [40, 40, 40]}
        ]

        cluster, boundingBox = cluster_items(items, 0.1)

        self.assertEqual(len(cluster), 5)
    

if __name__ == '__main__':
    unittest.main()
