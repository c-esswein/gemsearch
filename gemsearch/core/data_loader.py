import csv
import json

def traversePlaylists(filePath):
    with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['playlistId', 'userId', 'playlistName', 'tracksStr']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):
            # TODO: fix wrong quotes
            tracks = json.loads(line['tracksStr'].replace('\'', '"'))
            line['tracks'] = tracks
            yield line

def traversePlaylistTracks(filePath):
    for playlist in traversePlaylists(filePath):
        for track in playlist['tracks']:
            yield ({
                'type': 'playlist',
                'id': line['playlistId']
            },
            {
                'type': 'track',
                'id': track
            },
            1)

def traverseUserTrackInPlaylists(filePath):
    for playlist in traversePlaylists(filePath):
        for track in playlist['tracks']:
            yield ({
                'type': 'user',
                'id': line['userId']
            },
            {
                'type': 'track',
                'id': track
            },
            1)

def traverseTrackArtist(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['trackId', 'artistId']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):
            yield ({
                'type': 'track',
                'id': line['trackId']
            },
            {
                'type': 'artist',
                'id': line['artistId']
            },
            1)

def traverseTrackFeatures(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        for line in inFile:
            data = json.loads(line)
            for feature in data['features']:
                yield ({
                    'type': 'track',
                    'id': data['id']
                },
                {
                    'type': 'feature',
                    'id': feature
                },
                data['features'][feature])

def traverseTrackTag(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['trackId', 'tagId']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):
            yield ({
                'type': 'track',
                'id': line['trackId']
            },
            {
                'type': 'tag',
                'id': line['tagId']
            },
            1)

