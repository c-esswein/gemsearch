''' Generates embedding for api.
'''

from gemsearch.utils.logging import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traverseUserTrackInPlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseTypes

from gemsearch.core.type_counter import TypeCounter

from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.graph.weight_assigner import assign_edge_weights
from gemsearch.embedding import dim_reducer
from gemsearch.utils.timer import Timer

from pprint import pprint
import numpy as np

# ---- config ----
dataDir = 'data/tmp/'
outDir = 'data/tmp/'

SHOULD_EMBED = True
SHOULD_INDEX_ES = True

# ---- /config ----

logger.info('started api embedding with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_EMBED': SHOULD_EMBED,
    'SHOULD_INDEX_ES': SHOULD_INDEX_ES,
})

with Timer(logger=logger, message='api embedding') as t:

    if SHOULD_EMBED:
        print('------------- generate graph -------------')
        with Timer(logger=logger, message='graph generation') as t:

            graphGenerator = GraphGenerator(
                outDir+'graph.txt', 
                IdManager(outDir+'types.csv', 
                    typeHandlers = [TypeCounter()]
                )
            )

            graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
            graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
            graphGenerator.add(traverseTrackTag(dataDir+'track_tag.csv'))                
            graphGenerator.add(traverseUserTrackInPlaylists(dataDir+'playlist.csv'))

            graphGenerator.close_generation()

        if SHOULD_INDEX_ES:
            from gemsearch.query.elastic_search_filler import es_clear_indices, es_load_all_types
            with Timer(logger=logger, message='elastic search writer') as t:
                # clear all current entries in elastic search
                es_clear_indices()

                # insert all types
                es_load_all_types(traverseTypes(outDir+'types.csv'), 'music_index', 'music_type', dismissTypes = ['user'])
        

        print('------------- graph embedding -------------')

        with Timer(logger=logger, message='embedding') as t:
            # em = Node2vec(50, 1, 80, 10, 10, 1, 1, verbose=False)
            # em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')

            from gemsearch.embedding.default_embedder import embed_deepwalk
            embed_deepwalk(outDir+'graph.txt', outDir+'node2vec.em', modelFile=outDir+'word2vecModel.p')

        with Timer(logger=logger, message='weight assigning for graph') as t:
            geCalc = GeCalc()
            geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')

            assign_edge_weights(outDir+'graph.txt', outDir+'graph_w.txt', geCalc)


        with Timer(logger=logger, message='pca dimension reduction') as t:
            embedding = geCalc.embedding
            reduced = dim_reducer.pca(embedding)
            np.save(outDir+'pca.em', reduced)

        