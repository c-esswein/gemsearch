import numpy as np
#from gem.embedding.gf import GraphFactorization as gf
#from gem.embedding.node2vec import node2vec
from gemsearch.embedding.node2vec import Node2vec
from gem.utils import graph_util
from subprocess import call

class DefaultEmbedder:
    dimensions = 0

    def __init__(self, dimensions = 50):
        self.dimensions = dimensions

    def get_config_info(self):
        return "default embedding with " + str(self.dimensions) + " dimensions"

    def start_embedding(self, graphFile, outputFile):
        
        # Instatiate the embedding method with hyperparameters
        #em = gf(2, 100000, 1*10**-4, 1.0)
        #em = gf(self.dimensions, 100000, 1*10**-4, 1.0)
        
        # em = node2vec(2, 1, 80, 10, 10, 1, 1)
        # embed_graph(em, dataDir+'graph.txt', dataDir+'embedding.adj')

        em = Node2vec(50, 1, 80, 10, 10, 1, 1)
        em.learn_embedding(graphFile, outputFile)

        #node2vec_em(dataDir+'graph.txt')
        


# ------------- static functions ------------


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

if __name__ == '__main__':
    embedder = DefaultEmbedder()
    tmpDir = 'data/graph_100/'
    embedder.start_embedding(tmpDir+'graph.txt', tmpDir+'embedding.em')
    