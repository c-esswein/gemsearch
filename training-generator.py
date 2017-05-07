from pprint import pprint
import json
from Playlists import Playlists
from JSONEncoder import JSONEncoder

with open('keras-test/data/small-playlist-selection.json', "r", encoding="utf-8") as data_file:
    data = json.load(data_file)

playlists = Playlists()
result = []

for playlistKey in data:
    playlist = playlists.getPlaylistByKey(playlistKey)
    entry = {
        'key': playlist['key'],
        'playlist_id': playlist['_id']
    }
    entry['tracks'] = playlists.getTrackFeatures(playlist)
    result.append(entry)
    pprint('loaded ' + playlistKey)

pprint(len(result))

with open('keras-test/data/playlist-data.json', 'w') as outfile:
    for chunk in JSONEncoder().iterencode(result):
        outfile.write(chunk)
