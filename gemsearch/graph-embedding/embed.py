from gem.embedding.gf import GraphFactorization as gf
from gem.utils import graph_util
from pprint import pprint
import numpy as np

# TODO continue learning

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

def storeEmbedding(file_name, embedding):
    '''with open(file_name, 'w') as f:
        f.write('%d\n' % graph.number_of_nodes())'''
    np.savetxt(file_name, embedding)

def embed_graph(graphFile, embeddingFile = None):
    # Instatiate the embedding method with hyperparameters
    #em = gf(2, 100000, 1*10**-4, 1.0)
    em = gf(8, 200, 1*10**-4, 1.0)

    # Load graph
    graph = graph_util.loadGraphFromEdgeListTxt(graphFile)

    Y, t = em.learn_embedding(graph, is_weighted=True, no_python=False)

    if embeddingFile is not None:
        # store embedding
        storeEmbedding(embeddingFile, Y)
    else:
        return Y

if __name__ == '__main__':
    embed_graph('data/test1/graph.txt', 'data/test.txt')
    
    