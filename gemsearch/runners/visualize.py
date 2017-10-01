''' Reduce dimensions of embedding
'''

from gemsearch.utils.logging import setup_logging
setup_logging()
import logging
logger = logging.getLogger(__name__)

import numpy as np

from gemsearch.embedding import dim_reducer
from gemsearch.utils.timer import Timer
from gemsearch.embedding.ge_calc import read_native_embedding_file


tmpDir = 'data/graph_50_data/'
embedding = read_native_embedding_file(tmpDir+'node2vec.em')

logger.info('started dimension reducing, with', {
    'tmpDir': tmpDir
})

with Timer(logger=logger, message='svd') as t:
    reduced = dim_reducer.svd(embedding)
    np.save(tmpDir+'svd.em', reduced)

with Timer(logger=logger, message='pca') as t:
    reduced = dim_reducer.pca(embedding)
    np.save(tmpDir+'pca.em', reduced)
