from gemsearch.utils.logging import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseTypes, traverseUserTrackInPlaylistsObj

from gemsearch.core.type_counter import TypeCounter
from gemsearch.query.elastic_search_filler import es_clear_indices, es_load_all_types

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

from pprint import pprint

# ---- config ----
dataDir = 'data/graph_500/'
outDir = 'data/tmp/'

SHOULD_EMBED = True
SHOULD_INDEX_ES = True

TEST_PLAYLIST_SPLIT=0.2
MAX_PRECISION_AT=2
USE_USER_IN_QUERY = True
# ---- /config ----

logger.info('started playlist eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_EMBED': SHOULD_EMBED,
    'SHOULD_INDEX_ES': SHOULD_INDEX_ES,
    'TEST_PLAYLIST_SPLIT': TEST_PLAYLIST_SPLIT,
    'MAX_PRECISION_AT': MAX_PRECISION_AT,
    'USE_USER_IN_QUERY': USE_USER_IN_QUERY
})

with Timer(logger=logger, message='playlist_eval runner') as t:

    playlistEval = PlaylistQueryEvaluator(testSplit=TEST_PLAYLIST_SPLIT, maxPrecisionAt=MAX_PRECISION_AT, useUserContext=USE_USER_IN_QUERY)
    if USE_USER_IN_QUERY:
        trainingPlaylists = playlistEval.traverse(traversePlaylists(dataDir+'playlist.csv'))
    else:
        playlistEval.addPlaylists(traversePlaylists(dataDir+'playlist.csv'))

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

            if USE_USER_IN_QUERY:
                graphGenerator.add(traverseUserTrackInPlaylistsObj(trainingPlaylists))

            graphGenerator.close_generation()

        if SHOULD_INDEX_ES:
            with Timer(logger=logger, message='elastic search writer') as t:
                # clear all current entries in elastic search
                es_clear_indices()

                # insert all types
                es_load_all_types(traverseTypes(outDir+'types.csv'), 'music_index', 'music_type', dismissTypes = ['user'])
        

        print('------------- graph embedding -------------')

        with Timer(logger=logger, message='embedding') as t:
            em = Node2vec(50, 1, 80, 10, 10, 1, 1, verbose=False)
            em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')

    # load embedding
    with Timer(logger=logger, message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


    print('------------- evaluation -------------')

    with Timer(logger=logger, message='evaluation') as t:
        playlistEval.evaluate(geCalc)


    print('------------- done -------------')
