
from gemsearch.utils.tsne import tsne
from gemsearch.embedding.ge_calc import read_native_embedding_file
import numpy as np

em = read_native_embedding_file('data/graph_50_data/node2vec.em')

# tsneEm = tsne(em, 3, em.shape[1], 20.0)

np.savetxt('data/graph_50_data/embedding.em', em)
