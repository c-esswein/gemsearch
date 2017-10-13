''' Tag prediction evaluation runner: Hides tags of songs while training and
tries to predict tags while testing.
'''

from pprint import pprint
from gemsearch.utils.logging import setup_logging
setup_logging()
import logging
logger = logging.getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traverseUserTrackInPlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag

from gemsearch.core.type_counter import TypeCounter

from gemsearch.evaluation.tag_prediction_evaluator import TagPredictionEvaluator
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

# ---- config ----
dataDir = 'data/graph_50/'
outDir = 'data/tmp/'

TEST_TAG_SPLIT = 0.02
MAX_TOP_N_ACCURACY = 5

EMBEDDING_VERBOSE = False
# ---- /config ----

logger.info('started tag prediction eval with config: %s',{
    'dataDir': dataDir,
    'outDir': outDir,
    'TEST_TAG_SPLIT': TEST_TAG_SPLIT,
    'MAX_TOP_N_ACCURACY': MAX_TOP_N_ACCURACY
})

with Timer(logger=logger, message='playlist_eval runner') as t:
    tagPredictEval = TagPredictionEvaluator(testSplit=TEST_TAG_SPLIT, maxTopNAccuracy=MAX_TOP_N_ACCURACY)

    if SHOULD_EMBEDD:
        logger.info('------------- generate graph -------------')
        with Timer(logger=logger, message='graph generation') as t:

            graphGenerator = GraphGenerator(
                outDir+'graph.txt', 
                IdManager(outDir+'types.csv', 
                    typeHandlers = [TypeCounter()]
                )
            )

            graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
            graphGenerator.add(traverseUserTrackInPlaylists(dataDir+'playlist.csv'))
            graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
            graphGenerator.add(tagPredictEval.traverse(traverseTrackTag(dataDir+'track_tag.csv')))
            graphGenerator.close_generation()
    else:
        logger.info('load previously stored tags')
        # load previous split if runner has crashed or same split should be used again
        tagPredictEval.loadIntermediateTags()

    logger.info('------------- graph embedding -------------')
    
    # TODO: adapt to new embedding
    with Timer(logger=logger, message='embedding') as t:
        em = Node2vec(50, 1, 80, 10, 10, 1, 1, verbose=EMBEDDING_VERBOSE)
        em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')
    

    # load embedding
    with Timer(logger=logger, message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


    logger.info('------------- evaluation -------------')
    
    with Timer(logger=logger, message='evaluation') as t:
        tagPredictEval.evaluate(geCalc)

    logger.info('------------- done -------------')