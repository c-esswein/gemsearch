from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
import numpy as np
import networkx as nx
from deepwalk.node2vec_walks import Graph
from gensim.models import Word2Vec

def learn_embeddings(walks, dimensions=64, window=5, minCount=0, workers=1, sgdIter=1):
    '''
    Learn embeddings by optimizing the Skipgram objective using SGD.
    '''
    logger.info('start learning')        
    walks = [list(map(str, walk)) for walk in walks]
    model = Word2Vec(walks, size=dimensions, window=window, min_count=minCount, sg=1, workers=workers, iter=sgdIter)
    
    return model

def create_walks(graphFile, num_walks, walk_length, weighted=False):
    # read graph
    logger.info('load graph file')
    nx_G = None
    if weighted:
        nx_G = nx.read_edgelist(graphFile, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
    else:
        nx_G = nx.read_edgelist(graphFile, nodetype=int, create_using=nx.DiGraph())
        for edge in nx_G.edges():
            nx_G[edge[0]][edge[1]]['weight'] = 1

    # create walks
    G = Graph(nx_G)
    logger.info('preprocess transition probs')
    G.preprocess_transition_probs()
    logger.info('generate walks')
    walks = G.simulate_walks(num_walks, walk_length)

    return walks

def embeddNode2Vec(graphFile, num_walks, walk_length, weighted=False, \
    dimensions=64, window=5, minCount=0, workers=1, sgdIter=1):

    walks = create_walks(graphFile, num_walks, walk_length, weighted)
    return learn_embeddings(walks, dimensions, window, minCount, workers, sgdIter)

def embeddFromConfig(config):

    model = embeddNode2Vec(
        graphFile=config['input'], num_walks=config['number_walks'], walk_length=config['number_walks'], weighted=config['weighted'],
        dimensions=config['representation_size'], window=config['window_size'], workers=config['workers']
    )

    model.wv.save_word2vec_format(config['output'])

    return model
