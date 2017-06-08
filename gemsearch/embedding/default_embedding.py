import numpy as np
from gem.embedding.gf import GraphFactorization as gf
from gem.utils import graph_util

class DefaultEmbedding:
    dimensions = 0

    def __init__(self, dimensions = 10):
        self.dimensions = dimensions

    def get_config_info(self):
        return "default embedding with " + str(self.dimensions) + " dimensions"

    def start_embedding(self, dataDir):
        
        # Instatiate the embedding method with hyperparameters
        #em = gf(2, 100000, 1*10**-4, 1.0)
        em = gf(self.dimensions, 200, 1*10**-4, 1.0)

        embed_graph(em, dataDir+'graph.txt', dataDir+'embedding')

def embed_graph(em, graphFile, embeddingFile = None):
    graph = graph_util.loadGraphFromEdgeListTxt(graphFile)

    Y, t = em.learn_embedding(graph, is_weighted=True, no_python=False)

    if embeddingFile is not None:
        store_embedding(embeddingFile, Y)
    
    return Y, t

def store_embedding(file_name, embedding):
    np.savetxt(file_name, embedding)

if __name__ == '__main__':
    embedder = DefaultEmbedding()
    embedder.start_embedding('data/tmp_test/')
    