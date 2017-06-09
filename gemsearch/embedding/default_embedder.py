import numpy as np
from gem.embedding.gf import GraphFactorization as gf
from gem.utils import graph_util

class DefaultEmbedder:
    dimensions = 0

    def __init__(self, dimensions = 10):
        self.dimensions = dimensions

    def get_config_info(self):
        return "default embedding with " + str(self.dimensions) + " dimensions"

    def start_embedding(self, dataDir):
        
        # Instatiate the embedding method with hyperparameters
        #em = gf(2, 100000, 1*10**-4, 1.0)
        em = gf(self.dimensions, 200, 1*10**-4, 1.0)

        embed_graph(em, dataDir+'graph.txt', dataDir+'embedding.adj')


# ------------- static functions ------------

def embed_graph(em, graphFile, embeddingFile = None):
    ''' Embeds given graph with embedding method.
    '''
    graph = graph_util.loadGraphFromEdgeListTxt(graphFile)

    Y, t = em.learn_embedding(graph, is_weighted=True, no_python=False)

    if embeddingFile is not None:
        store_embedding(embeddingFile, Y)
    
    return Y, t

def store_embedding(file_name, embedding):
    ''' Stores embedding into file.
    '''
    np.savetxt(file_name, embedding)

# not used currently, use numpy.loadtxt() instead
def loadEmbedding(file_name):
    with open(file_name, 'r') as f:
        n, d = f.readline().strip().split()
        X = np.zeros((int(n), int(d)))
        for line in f:
            emb = line.strip().split()
            emb_fl = [float(emb_i) for emb_i in emb[1:]]
            X[int(emb[0]), :] = emb_fl
    return X

if __name__ == '__main__':
    embedder = DefaultEmbedding()
    embedder.start_embedding('data/tmp_test/')
    