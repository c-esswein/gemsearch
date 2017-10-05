
if __name__ == '__main__':
    from gemsearch.utils.logging import setup_logging
    setup_logging()

import logging
logger = logging.getLogger(__name__)

from gemsearch.storage.Tracks import Tracks
from gemsearch.crawler.skip_ids import SKIP_IDS
from gemsearch.crawler.last_fm_crawler import getTagsForTrack


def crawlTrack(track):
    ''' Starts all crawler necessary for new tracks.
    '''
    track['tags'] = getTagsForTrack(track)

    # TODO: add artist crawler

    return track

def crawlMissingTracks():
    ''' Finds all unprocessed tracks and starts crawlers.
    '''
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    batchLimit = 100
    tracks = trackCol.find({ 
        'tags' : { '$exists': False }, 
        '_id': { '$nin': SKIP_IDS }  # exclude blacklisted
    }).limit(batchLimit)

    count = tracks.count()
    if count > 0:
        logger.info('Started crawler for %s tracks', count)

    for track in tracks:
        logger.info('Started crawling track (uri: %s)', track['uri'])
        crawledTrack = crawlTrack(track)
        # trackCol.update_one({'_id': track['_id']}, {'$set': crawledTrack})

if __name__ == '__main__':
    crawlMissingTracks()
