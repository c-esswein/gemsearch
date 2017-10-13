''' Query extraction runner: 
'''

from gemsearch.utils.logging import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseTypes

from gemsearch.core.type_counter import TypeCounter
from gemsearch.query.elastic_search_filler import es_clear_indices, es_load_all_types

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator

from gemsearch.utils.timer import Timer
from pprint import pprint

# ---- config ----
dataDir = 'data/graph_50/'
outDir = 'data/tmp/'

SHOULD_WRITE_TYPES = False
SHOULD_INDEX_ES = False

# ---- /config ----

logger.info('started playlist eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_WRITE_TYPES': SHOULD_WRITE_TYPES,
    'SHOULD_INDEX_ES': SHOULD_INDEX_ES,
})

with Timer(logger=logger, message='playlist_eval runner') as t:

    if SHOULD_WRITE_TYPES:
        with Timer(logger=logger, message='traverse types') as t:

            idManager = IdManager(outDir+'types.csv', 
                typeHandlers = [TypeCounter()]
            )

            def addItems(traverser):
                ''' Add all items in traverser to idManager --> collects all unique items.
                '''
                for item1, item2, weight in traverser:
                    idManager.getId(item1)
                    idManager.getId(item2)

            addItems(traverseTrackFeatures(dataDir+'track_features.json'))
            addItems(traverseTrackArtist(dataDir+'track_artist.csv'))
            addItems(traverseTrackTag(dataDir+'track_tag.csv'))

            idManager.close()

    if SHOULD_INDEX_ES:
        with Timer(logger=logger, message='elastic search writer') as t:
            # clear all current entries in elastic search
            es_clear_indices()

            # insert all types
            es_load_all_types(traverseTypes(outDir+'types.csv'), 'music_index', 'music_type', dismissTypes = ['user'])
    
    
    evaluator = PlaylistQueryEvaluator()
    logger.info('Load playlists')
    evaluator.addPlaylists(traversePlaylists(dataDir+'playlist.csv'))

    logger.info('extract queries')
    extractedPlaylists = evaluator.extractQueries()

    logger.info('write extract queries to file')
    evaluator.writeTestLists(outDir+'playlists_with_queries.json')

    
    
    
logger.info('------------- done -------------')
