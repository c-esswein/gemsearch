''' Simple runner to count item types of extracted csv files.
'''

import gemsearch.core.data_loader as data_loader

dataDir = 'data/full_model/'

userTracks = data_loader.traverseUserTrackInPlaylists(dataDir + 'playlist.csv')
users = {}
for user, track, weight in userTracks:
    users[user['id']] = True
print(len(users)) 

trackTags = data_loader.traverseTrackTag(dataDir + 'track_tag.csv')
tags = {}
for track, tag, weight in trackTags:
    tags[tag['id']] = True
print(len(tags))
 
trackAlbum = data_loader.traverseTrackAlbum(dataDir + 'track_album.csv')
albums = {}
for track, album, weight in trackAlbum:
    albums[album['id']] = True
print(len(albums))

artistGenre = data_loader.traverseArtistGenre(dataDir + 'artist_genre.csv')
genres = {}
for artist, genre, weight in artistGenre:
    genres[genre['id']] = True
print(len(genres)) 

print('done')
