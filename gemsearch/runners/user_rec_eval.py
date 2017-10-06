''' Playlist evaluation runner: Extracts query from playlist name
and tries to predict playlist tracks.
'''

from gemsearch.utils.logging import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseTypes, traverseUserTrackInPlaylists

from gemsearch.core.type_counter import TypeCounter

from gemsearch.evaluation.user_evaluator import UserEvaluator
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

from pprint import pprint

# ---- config ----
dataDir = 'data/graph_50/'
outDir = 'data/rec/'

SHOULD_EMBED = True

TEST_SPLIT=0.2
MAX_PRECISION_AT=2
MIN_TRACKS_PER_USER = 20
# ---- /config ----

logger.info('started playlist eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_EMBED': SHOULD_EMBED,
    'TEST_SPLIT': TEST_SPLIT,
    'MAX_PRECISION_AT': MAX_PRECISION_AT,
    'MIN_TRACKS_PER_USER': MIN_TRACKS_PER_USER,
})

with Timer(logger=logger, message='playlist_eval runner') as t:

    userEval = UserEvaluator(testSplit=TEST_SPLIT, maxPrecisionAt=MAX_PRECISION_AT, minTracksPerUser = MIN_TRACKS_PER_USER)

    if SHOULD_EMBED:
        logger.info('------------- split training data -------------')
        trainingUserTrack = userEval.addUserTracks(traverseUserTrackInPlaylists(dataDir+'playlist.csv'))
        userEval.writeTestData(outDir+'user_eval.pk')

        logger.info('------------- generate graph -------------')
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
            graphGenerator.add(trainingUserTrack)
            graphGenerator.close_generation()


        logger.info('------------- graph embedding -------------')

        with Timer(logger=logger, message='embedding') as t:
            ''' from gemsearch.embedding.node2vec import Node2vec
            em = Node2vec(50, 1, 80, 10, 10, 1, 1, verbose=False)
            em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em') '''
            from gemsearch.embedding.default_embedder import embed_deepwalk
            embed_deepwalk(outDir+'graph.txt', outDir+'deepwalk.em', modelFile=outDir+'word2vecModel.p')

    else:
        # load stored test data if not in embedding mode
        logger.info('No embedding + splitting, loading previous split')
        userEval.loadTestData(outDir+'user_eval.pk')
    
    # load embedding
    with Timer(logger=logger, message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'deepwalk.em', outDir+'types.csv')


    logger.info('------------- evaluation -------------')

    with Timer(logger=logger, message='evaluation') as t:
        userEval.evaluate(geCalc)


    logger.info('------------- done -------------')
