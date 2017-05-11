from pprint import pprint
import json
from Playlists import Playlists
from Storage import Storage
from JSONEncoder import JSONEncoder

# loads playlists from file containing array of playlist keys
def loadPlaylistsFromKeyFile(filePath='keras-test/data/small-playlist-selection.json'):
    with open(filePath, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    
    playlists = Playlists()
    playlistData = map(lambda playlistKey: playlists.getPlaylistByKey(playlistKey),data)
    
    return loadTrackFeatures(playlistData)

# loads track features and maps them to playlist array
def loadTrackFeatures(data):
    playlistStorage = Playlists()

    result = []
    for playlist in data:
        entry = {
            'key': playlist['key'],
            'playlist_id': playlist['_id']
        }
        entry['tracks'] = playlistStorage.getTrackFeatures(playlist)
        result.append(entry)
        pprint('loaded ' + playlist['key'])

    pprint('Loaded Playlists:')
    print(len(result))
    return result

# store result in json file
def storeResultInFile(result, filePath):
    print('\nWrite result into file')
    with open(filePath, 'w') as outfile:
        for chunk in JSONEncoder().iterencode(result):
            outfile.write(chunk)


storage = Storage()
playlists = storage.getCollection('tmp_playlists_cleaned').find({}).limit(500)

result = loadTrackFeatures(playlists)
storeResultInFile(result, 'keras-test/data/playlist-data-full.json')