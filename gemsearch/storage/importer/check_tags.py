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

for row in readCsv('data/echonestDataset.csv'):
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
    })

    tracks[row['trackID']] = True


print('Playlists count: {}'.format(len(playLists.items())))
print('Tracks count: {}'.format(len(tracks.items())))



''' 
# insert playlists
storage = Storage()
playlistColl = storage.getCollection('playlists')

for playlist in playLists.values():
    print("insert: " + playlist['key'])
    playlistColl.insert(playlist)
 '''
print("import finished")