import csv
import json
import sys

# TODO: use json for playlists
csv.field_size_limit(500 * 1024 * 1024)

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
                'id': playlist['userId'],
                'name': playlist['userId']
            },
            {
                'type': 'track',
                'id': track
            },
            1)

def traverseUserTrackInPlaylistsObj(playlists):
    for playlist in playlists:
        for track in playlist['tracks']:
            yield ({
                'type': 'user',
                'id': playlist['userId'],
                'name': playlist['userId']
            },
            {
                'type': 'track',
                'id': track
            },
            1)

def traverseUserTrack(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['userId', 'trackId']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):            
            yield ({
                'type': 'user',
                'id': line['userId'],
                'name': line['userId']
            },
            {
                'type': 'track',
                'id': line['trackId']
            },
            1)

def traverseTrackArtist(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['trackId', 'artistId', 'artistName']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):
            yield ({
                'type': 'track',
                'id': line['trackId']
            },
            {
                'type': 'artist',
                'id': line['artistId'],
                'name': line['artistName']
            },
            1)

def traverseTrackFeatures(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        for line in inFile:
            data = json.loads(line)
            for feature in data['features']:
                yield ({
                    'type': 'track',
                    'name': data['name'],
                    'id': data['id']
                },
                {
                    'type': 'feature',
                    'id': 'feature::' + feature,
                    'name': feature
                },
                data['features'][feature])

def traverseTrackTag(filePath):
     with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['trackId', 'tagName']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):
            yield ({
                'type': 'track',
                'id': line['trackId']
            },
            {
                'type': 'tag',
                'name': line['tagName'],
                'id': 'tag::' + line['tagName']
            },
            1)


def traverseTypes(fileName):
    '''Reads type file
    '''
    with open(fileName, 'r', encoding="utf-8") as csvfile:
        # dict reader not possible because int cast is needed
        typeReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in typeReader:
            yield {
                'embeddingIndex': int(row[0]),
                'id': row[1],
                'type': row[2],
                'name': row[3]
            }
