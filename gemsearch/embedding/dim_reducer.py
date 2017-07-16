''' Utilities to reduce dimension of embedding.
'''

from sklearn import manifold, decomposition
import numpy as np

def tsne(embedding, targetDimension=3):
    tsne = manifold.TSNE(n_components=targetDimension, init='pca', random_state=0)
    X_tsne = tsne.fit_transform(embedding)
    return X_tsne

def mds(embedding, targetDimension=3):
    clf = manifold.MDS(n_components=targetDimension, n_init=1, max_iter=100)
    X_mds = clf.fit_transform(embedding)
    print("Done. Stress: %f" % clf.stress_)
    return X_mds

def svd(embedding, targetDimension=3):
    return decomposition.TruncatedSVD(n_components=targetDimension).fit_transform(embedding)

def pca(embedding, targetDimension=3):
    return decomposition.PCA(n_components=targetDimension).fit_transform(embedding)
    

if __name__ == '__main__':
    from gemsearch.utils.timer import Timer
    from gemsearch.embedding.ge_calc import read_native_embedding_file

    tmpDir = 'data/graph_50_data/'
    embedding = read_native_embedding_file(tmpDir+'node2vec.em')
    
    with Timer(message='mds') as t:
        reduced = svd(embedding)
        print("write")
        np.savetxt(tmpDir+'reduced.md', reduced)

    