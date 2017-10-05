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
SHOULD_INDEX_ES = False

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

name = 'node2vec_dim3_wLen3_nWalks3'
# load embedding
with Timer(logger=logger, message='ge calc initializing') as t:
    geCalc = GeCalc()
    geCalc.load_node2vec_data(outDir+name+'.em', outDir+'types.csv')


print('------------- evaluation -------------')
playlistEval = PlaylistQueryEvaluator(testSplit=TEST_PLAYLIST_SPLIT, maxPrecisionAt=MAX_PRECISION_AT, useUserContext=USE_USER_IN_QUERY)
playlistEval.addPlaylists(traversePlaylists(dataDir+'playlist.csv'))

with Timer(logger=logger, message='evaluation') as t:
    playlistEval.evaluate(geCalc)
