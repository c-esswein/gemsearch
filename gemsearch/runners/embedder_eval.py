''' Playlist evaluation runner: Extracts query from playlist name
and tries to predict playlist tracks.
'''

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
# dataDir = 'data/graph_15000/'
dataDir = 'data/graph_50/'
outDir = 'data/embedder_eval/'

SHOULD_EMBED = True
SHOULD_INDEX_ES = True

TEST_PLAYLIST_SPLIT=0.2
MAX_PRECISION_AT=2
USE_USER_IN_QUERY = False
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

def get_embedder():
    for dim in [3, 5, 8, 15, 25, 30, 50, 128]:
        for wLen in [3, 5, 8, 15, 25, 30, 50]:
            for nWalks in [3, 5, 8, 15, 25, 30, 50]:
                logger.info('Create node2vec %s', {
                    'dim': dim, 'walk length': wLen, 'number of walks': nWalks
                })
                # d, max_iter(Number of epochs in SGD), wLen, nWalks, cSize=Context size, ret_p, inout_p,
                em = Node2vec(dim, 1, wLen, nWalks, 10, 1, 1, verbose=False)
                name = 'node2vec_dim{}_wLen{}_nWalks{}'.format(dim, wLen, nWalks)
                yield name, em 
    
    ''' from gemsearch.embedding.default_embedder import embed_deepwalk
    embed_deepwalk(outDir+'graph.txt', outDir+'deepwalk.em', modelFile=outDir+'word2vecModel.p') '''

with Timer(logger=logger, message='playlist_eval runner') as t:

    evalResults = {}
    playlistEval = PlaylistQueryEvaluator(testSplit=TEST_PLAYLIST_SPLIT, maxPrecisionAt=MAX_PRECISION_AT, useUserContext=USE_USER_IN_QUERY)
    if USE_USER_IN_QUERY:
        trainingPlaylists = playlistEval.traverseAndSplitPlaylists(traversePlaylists(dataDir+'playlist.csv'))
        playlistEval.writeTestLists(outDir)
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

        for name, em in get_embedder():
            logger.info('started testing %s', name)

            with Timer(logger=logger, message='embedding') as t:
                em.learn_embedding(outDir+'graph.txt', outDir+name+'.em')

            # load embedding
            with Timer(logger=logger, message='ge calc initializing') as t:
                geCalc = GeCalc()
                geCalc.load_node2vec_data(outDir+name+'.em', outDir+'types.csv')


            print('------------- evaluation -------------')

            with Timer(logger=logger, message='evaluation') as t:
                result = playlistEval.evaluate(geCalc)

                # store result
                evalResults[name] = result


    print('------------- done -------------')
    logger.info('Total results: %s', evalResults)
