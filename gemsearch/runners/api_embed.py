''' Generates embedding for api.
'''

from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
import gemsearch.core.data_loader as data_loader

from gemsearch.core.type_counter import TypeCounter

from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.graph.weight_assigner import assign_edge_weights
from gemsearch.embedding import dim_reducer
from gemsearch.utils.timer import Timer

from pprint import pprint
import numpy as np

# ---- config ----
dataDir = 'data/graph_50/'
outDir = 'data/api/'

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
            idManager = IdManager(outDir+'types.csv', 
                typeHandlers = [TypeCounter()]
            )
            graphGenerator = GraphGenerator(
                outDir+'graph.txt', idManager
            )

            # graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
            # add tracks without features
            for track, feature, weight in data_loader.traverseTrackFeatures(dataDir+'track_features.json'):
                idManager.getId(track)

            graphGenerator.add(data_loader.traverseTrackArtist(dataDir+'track_artist.csv'))
            graphGenerator.add(data_loader.traverseTrackTag(dataDir+'track_tag.csv'))                
            graphGenerator.add(data_loader.traverseUserTrackInPlaylists(dataDir+'playlist.csv'))
            # TODO: enable + share with embed_new_users
            # graphGenerator.add(data_loader.traverseUserTrack(dataDir+'user_tracks.csv'))

            graphGenerator.close_generation()

        if SHOULD_INDEX_ES:
            from gemsearch.query.elastic_search_filler import es_clear_indices, es_load_all_types
            with Timer(logger=logger, message='elastic search writer') as t:
                # clear all current entries in elastic search
                es_clear_indices()

                # insert all types
                es_load_all_types(data_loader.traverseTypes(outDir+'types.csv'), 'music_index', 'music_type', dismissTypes = ['user'])
        

        print('------------- graph embedding -------------')

        with Timer(logger=logger, message='embedding') as t:
            from gemsearch.embedding.default_embedder import embed_deepwalk
            embed_deepwalk(outDir+'graph.txt', outDir+'embedding.em', modelFile=outDir+'word2vecModel.p')

        with Timer(logger=logger, message='weight assigning for graph') as t:
            geCalc = GeCalc()
            geCalc.load_node2vec_data(outDir+'embedding.em', outDir+'types.csv')

            assign_edge_weights(outDir+'graph.txt', outDir+'graph_w.txt', geCalc)


        with Timer(logger=logger, message='pca dimension reduction') as t:
            embedding = geCalc.embedding
            reduced = dim_reducer.pca(embedding)
            np.save(outDir+'pca.em', reduced)

        