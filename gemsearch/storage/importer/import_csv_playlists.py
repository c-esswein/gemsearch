import csv
from pprint import pprint
from gemsearch.storage.Storage import Storage

def readCsv(filename):
    with open(filename, "r", encoding="utf-8") as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in datareader:
            yield row

# create playlist map
playLists = dict()

    # 'username': row[0],
    # 'track_uri': row[1],
    # 'name': row[2],

for row in readCsv('data/playlist.csv'):
    playlistKey = row[0] + '_' + row[2]
    if not playlistKey in playLists:
        playLists[playlistKey] = {
            'key': playlistKey,
            'username': row[0],
            'name': row[2],
            'tracks': []
        }
    playLists[playlistKey]['tracks'].append({
        'track_uri': row[1]
    })

# insert playlists
storage = Storage()
playlistColl = storage.getCollection('playlists')

for playlist in playLists.values():
    print("insert: " + playlist['key'])
    playlistColl.insert(playlist)

print("import finished")