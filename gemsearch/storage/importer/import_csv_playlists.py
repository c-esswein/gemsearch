''' Runner to import additional dbis spotify data.
'''

import csv
from pprint import pprint
from gemsearch.storage.Storage import Storage

def readCsv(filename):
    with open(filename, "r", encoding="utf-8") as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in datareader:
            yield row


# create playlist map
playLists = dict()
tracks = dict()

# load data
for row in readCsv('../dbis-data/spotifyPlaylistDataset/playlistDataset.csv'):
    playlistKey = row['userID'] + '_' + row['playlistName']
    if not playlistKey in playLists:
        playLists[playlistKey] = {
            'key': playlistKey,
            'username': row['userID'],
            'name': row['playlistName'],
            'tracks': []
        }
    playLists[playlistKey]['tracks'].append({
        'track_uri': row['trackID']
        # TODO: track id is not set!
    })

    # tracks[row['trackID']] = True


print('Playlists count: {}'.format(len(playLists.items())))
# print('Tracks count: {}'.format(len(tracks.items())))


# insert playlists
storage = Storage()
playlistColl = storage.getCollection('playlists')

missing = []
for playlist in playLists.values():
    dbPlaylist = playlistColl.find_one({'key': playlist['key']})
    if dbPlaylist is None:
        print("missing: " + playlist['key'])
        missing.append(playlist)

        # insert
        # playlistColl.insert_one(playlist)

        # collect tracks
        for track in playlist['tracks']:
            tracks[track] = True
            

print('Playlists missing count: {}'.format(len(missing)))

# check missing tracks
missingTracks = []
trackColl = storage.getCollection('tracks')
for trackUri in tracks:
    dbTrack = trackColl.find_one({'uri': trackUri})
    if dbTrack is None:
        missingTracks.append(dbTrack)

# check missing tracks

print("missing tracks: " + str(len(missingTracks)))
pprint(missingTracks)

print("import finished")
