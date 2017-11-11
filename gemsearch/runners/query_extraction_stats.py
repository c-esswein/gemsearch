''' Query extraction stats runner. 
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator

from gemsearch.utils.timer import Timer
from pprint import pprint
import collections

# ---- config ----
outDir = 'data/queries/'


# ---- /config ----

logger.info('started query extraction stats with config: %s', {
    'outDir': outDir,
})

with Timer(logger=logger, message='query extraction stats runner') as t:


    evaluator = PlaylistQueryEvaluator()
    logger.info('Load playlists')
    evaluator.loadTestLists(
        outDir + 'test_playlists_queries.json', containsQueries=True)
    logger.info('Total playlist count %s', len(evaluator._playlists))

    queryKeys = ['simple_first_match', 'simple_first_two_match', 'multiple_queries']
    stats = {}
    for key in queryKeys:
        stats[key] = collections.Counter()

    for playlist in evaluator._playlists:
        for key in queryKeys:
            query = playlist['extracted_queries'][key]
            statCounter = stats[key]

            for queryId in query:
                # get type
                if queryId.startswith('spotify:artist:'):
                    statCounter['artist'] += 1
                elif queryId.startswith('spotify:track:'):
                    statCounter['track'] += 1
                elif queryId.startswith('spotify:album:'):
                    statCounter['album'] += 1
                elif queryId.startswith('tag::'):
                    statCounter['tag'] += 1
                elif queryId.startswith('genre::'):
                    statCounter['genre'] += 1
                else:
                    print(queryId)

    for key in queryKeys:
        print(key)
        pprint(stats[key])


logger.info('------------- done -------------')
