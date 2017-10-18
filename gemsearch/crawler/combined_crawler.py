
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.storage.Tracks import Tracks
from gemsearch.storage.Storage import Storage
from gemsearch.crawler.skip_ids import SKIP_IDS
from gemsearch.crawler.last_fm_crawler import getTagsForTrack
from gemsearch.crawler.spotify_api import crawlArtist, crawlTrack, getSpotipyInstance


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
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()
    artistCol = Storage().getCollection('artists')

    batchLimit = 100
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

def crawlMissingTracks():
    ''' Crawl tracks and tags which are not in db yet.
    '''
    storage = Storage()
    missingTrackCol = storage.getCollection('tmp_missing_tracks')
    trackCol = storage.getCollection('tracks')
    artistCol = storage.getCollection('artists')

    sp = getSpotipyInstance()

    from pprint import pprint
    
    trackIds = missingTrackCol.find({})
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
        logger.info('crawled track: %s', trackUri)

        # check if artist is in db
        crawlTrackArtists(sp, track, artistCol)


if __name__ == '__main__':
    crawlMissingTracks()
