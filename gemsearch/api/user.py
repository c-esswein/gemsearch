import spotipy
from gemsearch.storage.Storage import Storage
from pymongo import UpdateOne
from pymongo.bulk import BulkWriteError
from pprint import pprint

def getUser(userName):
    '''Returns user from storage or None if not present.
    '''
    storage = Storage()
    usersCol = storage.getCollection('users')
    user = usersCol.find_one({'id': userName})
    return user


def syncUserMusic(token):
    '''Load user spotify music library and store it into db
    '''

    if not token:
        raise Exception('no token given')

    # load user and user music from spotify api
    sp = spotipy.Spotify(auth=token)
    user = sp.current_user()
    tracks = getSpotifyUserMusic(sp)

    # only store track id and uri in user obj
    user['tracks'] = [{
        'added_at': trackMeta['added_at'],
        'track_uri': trackMeta['track']['uri'],
        'track_id': trackMeta['track']['id'],
    } for trackMeta in tracks]
    
    # store user data (insert new or replace existing user)
    storage = Storage()
    usersCol = storage.getCollection('users')
    usersCol.replace_one(filter={'id': user['id']}, replacement=user, upsert=True)

    # store new tracks
    tracksCol = storage.getCollection('tracks')
    try:
        tracksCol.bulk_write([
            UpdateOne(
                {'uri': track['track']['uri']}, 
                {'$set': track['track']},
                upsert=True
            )
        for track in tracks])
    
    except BulkWriteError as bwe:
        print(bwe.details)
        raise

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

    count = usersCol.aggregate([
        # select user
        { "$match" : { 'id' : userName } },
        { "$unwind": "$tracks" },

        # join with tracks collection
        { "$lookup": {
                "from": 'tracks',
                'localField': 'tracks.track_uri',
                'foreignField': 'uri',
                'as': 'trackData'
            }
        },
        
        # find not matching songs
        { "$match" : { 'trackData' : { "$eq": [] } } },
        
        { "$project": {
            "track_id" : "$tracks.track_id",
            "track_uri": "$tracks.track_uri",
        }},

        { "$count" : "track_count" }
    ])

    pprint(list(count))



if __name__ == '__main__':
    token = 'BQD6hF9Pn2-DyY8o-5Lk2IMm1Vbdq99pCTbB4TU1CzXn5D6Ocvzbgcz2sZ5ubMUl8WNdPvh6lIw-BCfMbBTK8E7hF021Rbo1A7K2FYuQMAd2qdYGziXe52B9oswKrlSn5RGQI1EbHa8CiXeLmNBtfQ'
    syncUserMusic(token)
    # getMissingTracks('')
