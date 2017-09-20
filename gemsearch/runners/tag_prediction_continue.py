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
dataDir = 'data/graph_10000/'
outDir = 'data/graph_10000_tag_eval/'

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

    # load previous test tags

    tagPredictEval.loadIntermediateTags()

    # load embedding
    with Timer(logger=logger, message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


    logger.info('------------- evaluation -------------')
    
    with Timer(logger=logger, message='evaluation') as t:
        tagPredictEval.evaluate(geCalc)

    logger.info('------------- done -------------')