import spotipy
from gemsearch.storage.Storage import Storage

def isUserInDb(userName):
    '''Returns True if user is already synced in db
    '''
    storage = Storage()
    usersCol = storage.getCollection('users')
    user = usersCol.find_one({'id': userName})

    return not (user is None)

def syncUserMusic(token):
    '''Load user spotify music library and store it into db
    '''

    if not token:
        raise Exception('no token given')

    # load user and user music from spotify api
    sp = spotipy.Spotify(auth=token)
    user = sp.current_user()
    user['tracks'] = getSpotifyUserMusic(sp)
    
    # store data (insert new or replace existing user)
    storage = Storage()
    usersCol = storage.getCollection('users')
    usersCol.replace_one(filter={'id': user['id']}, replacement=user, upsert=True)

def getSpotifyUserMusic(sp):
    '''Load complete user music library
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


if __name__ == '__main__':
    token = ''
    syncUserMusic(token)
