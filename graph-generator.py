"""
Generates graph training set from mongodb
"""
from pprint import pprint
from Playlists import Playlists
from Tracks import Tracks
from Storage import Storage
import csv

typeFile = open('data/types-all.csv', 'w', encoding="utf-8")
typeWriter = csv.writer(typeFile, delimiter=',', lineterminator='\n',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

idCounter = 0
lookupDict = {}

# get uid and write type info
def getId(uidObj, type, name, uri = ""):
    global idCounter
    uid = str(uidObj)
    if not uid in lookupDict:
        lookupDict[uid] = idCounter
        typeWriter.writerow([idCounter, type, uid, name, uri])
        idCounter += 1
    
    return str(lookupDict[uid])


def get_items(limit):
    ''' Generator with all items in db.
    '''
    playlists = Storage().getCollection('tmp_playlists_cleaned').find({}).limit(limit)
    tracksRepo = Tracks()
        
    for playlist in playlists:
        userId = getId(playlist['username'], 'user', playlist['username'])
        playlistId = getId(playlist['_id'], 'playlist', playlist['name'])
        
        yield {
            'type': 'user-playlist',
            'user': userId,
            'playlist': playlistId
        }

        for track in playlist['tracks']:
            trackData = tracksRepo.getTrackById(track['track_id'])
            trackId = getId(track['track_id'], 'track', trackData['name'], trackData['uri'])
            
            yield {
                'type': 'playlist-track',
                'user': userId,
                'playlist': playlistId,
                'track': trackId
            }

            # --- artists ---
            artists = []
            for artist in trackData['artists']:
                artistId = getId(artist['id'], 'artist', artist['name'], artist['uri'])
                artists.append(artist['name'])

                yield {
                    'type': 'track-artist',
                    'user': userId,
                    'playlist': playlistId,
                    'track': trackId,
                    'artist': artistId
                }
            
            # artistName = ' ++ '.join(artists)

            # --- tags ---
            if 'tags' in trackData:
                for tag in trackData['tags']:
                    tagId = getId(tag['name'], 'tag', tag['name'])

                    yield {
                        'type': 'track-tag',
                        'user': userId,
                        'playlist': playlistId,
                        'track': trackId,
                        'tag': tagId
                    }

def write_connection(f, item1, item2, weight = 1):
    #r.write(item1+' '+item2+ '\n')
    pprint((item1, item2))

def create_biparite_graph(outfile, limit):
    for item in get_items(limit):
        if item['type'] == 'user-playlist':
            write_connection(outfile, item['user'], item['playlist'])
        if item['type'] == 'track-artist':
            write_connection(outfile, item['user'], item['artist'])
        if item['type'] == 'playlist-track':
            write_connection(outfile, item['user'], item['track'])
        # tags missing

def create_normal_graph(outfile, limit):
    for item in get_items(limit):
        if item['type'] == 'user-playlist':
            write_connection(outfile, item['user'], item['playlist'])
        if item['type'] == 'track-artist':
            write_connection(outfile, item['track'], item['artist'])
            write_connection(outfile, item['user'], item['playlist'])
        if item['type'] == 'track-tag':
            write_connection(outfile, item['track'], item['tag'])
        if item['type'] == 'playlist-track':
            write_connection(outfile, item['playlist'], item['track'])


with open('data/graph_200p.txt', 'w') as outfile:
    create_normal_graph(outfile, 10)

print("here")