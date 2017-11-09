''' Playlist query extractor: Extracts queries from playlist names and creates stats.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

import gemsearch.core.data_loader as data_loader

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

from pprint import pprint

# ---- config ----

dataDir = 'data/graph_50/'
outDir = 'data/tmp/'


PRECISION_AT = [5, 10]
USE_USER_IN_QUERY = True

# ---- /config ----

logger.info('started playlist eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'PRECISION_AT': PRECISION_AT,
    'USE_USER_IN_QUERY': USE_USER_IN_QUERY
})

with Timer(logger=logger, message='playlist_eval runner') as t:

    playlistEval = PlaylistQueryEvaluator(
        precisionAt=PRECISION_AT,
        useUserContext=USE_USER_IN_QUERY)

    # reload existing split
    if USE_USER_IN_QUERY:
        playlistEval.loadTestLists(outDir + 'test_playlists.json')
    else:
        playlistEval.addPlaylists(
            data_loader.traversePlaylists(dataDir + 'playlist.csv'))

    playlistEval.extractQueries()

    ''' # load embedding
    with Timer(logger=logger, message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir + 'deepwalk.em', outDir + 'types.csv')

    logger.info('------------- evaluation -------------')

    with Timer(logger=logger, message='evaluation') as t:
        res = playlistEval.evaluate(geCalc)

        # transform to array
        resList = [{'key': resKey, 'values': res[resKey]} for resKey in res]
        resList.sort(key=lambda runRes: runRes['values']['precision'])
        pprint(resList) '''

    # write test lists with extracted queries
    playlistEval.writeTestLists(outDir + 'test_playlists_queries.json')

    print('------------- done -------------')
