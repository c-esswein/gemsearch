''' Generates datasets which are splitted based on artist diversity.
One set contains only playlists with one single artist, the other contains multiple artists
'''

from gemsearch.core.data_generator import DataGenerator
from gemsearch.storage.Storage import Storage
from .same_artists_keys import DIVERSE_ARTIST_KEYS

singleArtists = DataGenerator('data/model_single_artists/')
multipleArtists = DataGenerator('data/model_multiple_artists/')

playlistCol = Storage().getCollection('playlists')
playlists = playlistCol.find({}, no_cursor_timeout=True)

for playlist in playlists:
    if playlist['key'] in DIVERSE_ARTIST_KEYS:
        multipleArtists.writePlaylist(playlist)
    else:
        singleArtists.writePlaylist(playlist)


print('done')
