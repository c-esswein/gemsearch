from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

import spotipy
from gemsearch.storage.Storage import Storage
from pymongo import UpdateOne
from pymongo.bulk import BulkWriteError
from pprint import pprint
import hashlib
from datetime import datetime

def getUser(userName):
    '''Returns user from storage or None if not present.
    '''
    storage = Storage()
    usersCol = storage.getCollection('users')
    user = usersCol.find_one({'userName': userName})
    return user

def getUserNameHash(userName):
    return hashlib.sha256(userName).hexdigest()

def syncUserMusic(userName, token):
    '''Load user spotify music library and store it into db. Returns number
    of synced tracks.
    '''

    if not token:
        raise Exception('no token given')

    logger.info('synced user %s', userName)

    # load user and user music from spotify api
    sp = spotipy.Spotify(auth=token)
    # user = sp.current_user()
    tracks = getSpotifyUserMusic(sp)

    # only store track id and uri in user obj
    userTracks = [{
        'added_at': trackMeta['added_at'],
        'track_uri': trackMeta['track']['uri'],
        'track_id': trackMeta['track']['id'],
    } for trackMeta in tracks]
    
    # store user data (insert new or replace existing user)
    storage = Storage()
    usersCol = storage.getCollection('users')
    dbUser = getUser(userName)
    update = {
        'tracks': userTracks,
        'latest_sync': datetime.now(),
        'userStatus': 'SPOTIFY_SYNCED'
    }
    if dbUser is None:
        # create new user
        dbUser = update
        dbUser['userName'] = userName
        dbUser['created'] = datetime.now()
        usersCol.insert_one(dbUser)
    else:
        # update user
        if dbUser['userStatus'] == 'EMBEDDED':
            update['userStatus'] = 'PARTIAL_EMBEDDED'
        usersCol.update_one(filter={'_id': dbUser['_id']}, update=update, replacement=update)

    # store new tracks
    tracksCol = storage.getCollection('tracks')
    try:
        bulkResult = tracksCol.bulk_write([
            UpdateOne(
                {'uri': track['track']['uri']}, 
                {'$set': track['track']},
                upsert=True
            )
        for track in tracks])
    
    except BulkWriteError as bwe:
        print(bwe.details)
        raise

    pprint(bulkResult)
    missingTracks = 0
    # TODO: return number of insert / upsert tracks --> unkown tracks

    return len(tracks), missingTracks

def getSpotifyUserMusic(sp):
    '''Load complete user music library from spotify.
    '''
    tracks = []

    offset = 0
    limit = 50
    while True:
        print('get ' + str(offset))
        response = sp.current_user_saved_tracks(limit=limit, offset=offset)
        tracks.extend(response['items'])

        if not ('next' in response) or response['next'] is None:
            break

        offset = offset + limit

    return tracks

def getMissingTracks(userName):
    ''' Find missing tracks in db from user library.
    '''
    storage = Storage()
    usersCol = storage.getCollection('users')

    queryRes = usersCol.aggregate([
        # select user
        { "$match" : { 'userName' : userName } },
        { "$unwind": "$tracks" },

        # join with tracks collection
        { "$lookup": {
                "from": 'tracks',
                'localField': 'tracks.track_uri',
                'foreignField': 'uri',
                'as': 'trackData'
            }
        },
        
        # find uncrawled tracks --> check for missing track['gemsearch_status']
        { "$match" : { 'gemsearch_status' : { '$exists': False} } },
        
        #{ "$project": {
        #    "track_id" : "$tracks.track_id",
        #    "track_uri": "$tracks.track_uri",
        #}},

        { "$count" : "track_count" }
    ])

    rows = list(queryRes)
    if len(rows) < 1:
        return 0
    else:
        missingCount = rows[0]['track_count']
        return missingCount


def getNewUsersForEmbedding():
    ''' Returns all new users which are not yet embedded but 
    ready (all tracks crawled).
    '''
    newUsers = Storage().getCollection('users').find({'userStatus': {'$in': ['SPOTIFY_SYNCED', 'PARTIAL_EMBEDDED']}})
    # check if new tracks are already crawled:
    res = []
    for user in newUsers:
        if getMissingTracks(user['userName']) < 1:
            res.append(user)
    
    return res

def setUsersState(users, newState):
    ''' Updates user state for given users
    '''
    userCol = Storage().getCollection('users')

    for user in users:
        user['userStatus'] = newState
        userCol.update_one({'_id': user['_id']}, user)


if __name__ == '__main__':
    token = ''
    syncUserMusic(token)
    # getMissingTracks('')
