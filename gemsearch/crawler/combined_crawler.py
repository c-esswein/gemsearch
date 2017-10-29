
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.storage.Tracks import Tracks
from gemsearch.storage.Storage import Storage
from gemsearch.crawler.last_fm_crawler import getTagsForTrack
from gemsearch.crawler.spotify_api import crawlArtist, crawlTrack, getSpotipyInstance
import time

def crawlTrackMeta(track):
    ''' Starts all crawler necessary for new tracks.
    '''
    track['tags'] = getTagsForTrack(track)

    return track

def crawlTrackArtists(sp, track, artistCol):
    for artist in track['artists']:    
        dbArtist = artistCol.find_one({'uri': artist['uri']})

        if dbArtist is None:
            crawledArtist = crawlArtist(sp, artist['id'])
            
            if crawledArtist is None:
                logger.warn('artists not found at api: ' + str(artist['uri']))
            else:
                artistCol.insert_one(crawledArtist)
                logger.info('crawled artist: %s', artist['uri'])

def crawlNewTracks():
    ''' Finds all unprocessed tracks and starts crawlers.
    '''
    storage = Storage()
    trackCol = storage.getCollection('tracks')
    artistCol = storage.getCollection('artists')

    batchLimit = 10000
    tracks = trackCol.find({ 
        'gemsearch_status' : { '$exists': False }
    }).limit(batchLimit)

    count = tracks.count()
    if count > 0:
        logger.info('Started crawler for %s tracks', count)

    sp = getSpotipyInstance()
    
    for track in tracks:
        logger.info('Started crawling track (uri: %s)', track['uri'])
        crawledTrack = crawlTrackMeta(track)
        # transition state
        crawledTrack['gemsearch_status'] = 'CRAWLED'
        trackCol.update_one({'_id': track['_id']}, {'$set': crawledTrack})

        crawlTrackArtists(sp, track, artistCol)

currentSkip = 0
def crawlMissingTracks(skip = 0):
    ''' Crawl tracks and tags which are not in db yet.
    '''
    global currentSkip
    storage = Storage()
    missingTrackCol = storage.getCollection('tmp_missing_tracks')
    trackCol = storage.getCollection('tracks')
    artistCol = storage.getCollection('artists')

    sp = getSpotipyInstance()

    currentSkip = skip
    
    trackIds = missingTrackCol.find({}).skip(skip)
    for trackId in trackIds:
        trackUri = trackId['_id']

        # crawl track
        track = crawlTrack(sp, trackUri)

        if track is None:
            logger.warn('track not found at api: ' + str(trackUri))
            continue

        # crawl tags
        track = crawlTrackMeta(track)

        # store track
        track['gemsearch_status'] = 'CRAWLED'        
        trackCol.insert_one(track)
        currentSkip += 1
        logger.info('crawled track (%s): %s', currentSkip, trackUri)

        # check if artist is in db
        crawlTrackArtists(sp, track, artistCol)


def continueCrawling(skip):
    ''' Continue crawling starting from skip.
    '''
    global currentSkip
    try:
        crawlMissingTracks(skip)
    except Exception as e:
        logger.error('crached:', exc_info=True)
        slack_error_message('track crawler crashed (will continue): ', e)
        time.sleep(120)
        continueCrawling(currentSkip)

if __name__ == '__main__':
    from gemsearch.utils.slack import slack_send_message, slack_error_message
    import sys

    # check if skip is in argv
    skip = 0
    for arg in sys.argv:
        if arg.startswith('--skip='):
            skip = int(arg.replace('--skip=', ''), 10)
    
    logger.info('started missing track crawler, will skip first: %s', skip)    

    continueCrawling(skip)
    slack_send_message('track crawler is done')
