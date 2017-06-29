import numpy as np
#from gem.embedding.gf import GraphFactorization as gf
#from gem.embedding.node2vec import node2vec

from gem.utils import graph_util


# TODO: add more embedders and more options, use in evaluations
def create_embedders():
    from gemsearch.embedding.node2vec import Node2vec

    for dimension in [3, 5, 10, 20, 50]:
        em = Node2vec(dimension, 1, 80, 10, 10, 1, 1, verbose=False)
        yield em


# CHECK: not in use
def embed_graph(em, graphFile, embeddingFile = None):
    ''' Embeds given graph with embedding method.
    '''
    graph = graph_util.loadGraphFromEdgeListTxt(graphFile)
    print('Graph with {} nodes and {} edges'.format(graph.number_of_nodes(), graph.number_of_edges()))

    Y, t = em.learn_embedding(graph, is_weighted=True, no_python=True)
    print('%% embedding took: {}s'.format(t))

    if embeddingFile is not None:
        store_embedding(embeddingFile, Y)
    
    return Y, t

def store_embedding(file_name, embedding):
    ''' Stores embedding into file.
    '''
    np.savetxt(file_name, embedding)


def embed_gf(graphFile, outputFile):
    from gem.embedding.gf import GraphFactorization as gf
    em = gf(50, 100000, 1*10**-4, 1.0)
    X, t = em.learn_embedding(edge_f=graphFile, is_weighted=True)
    store_embedding(outputFile, X)

def embed_hope(graphFile, outputFile):
    from gem.embedding.hope import HOPE
    em = HOPE(50, 0.01)
    X, t = em.learn_embedding(edge_f=graphFile, is_weighted=True)
    store_embedding(outputFile, X)

if __name__ == '__main__':
    tmpDir = 'data/run1/'
    # embed_hope(tmpDir+'graph.txt', tmpDir+'hope.em')
    embed_gf(tmpDir+'graph.txt', tmpDir+'gf.em')

    print("done")