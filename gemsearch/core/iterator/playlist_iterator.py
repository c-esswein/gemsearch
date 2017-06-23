"""Iterates over all items in db
"""

from gemsearch.core.iterator.item_iterator import ItemIterator
from gemsearch.storage.Storage import Storage
from gemsearch.storage.Tracks import Tracks

# TODO integrate albums

class PlaylistIterator(ItemIterator):

    def iterate(self, typeHandlers):
        ''' Generator with all items in db.
        '''
        super(PlaylistIterator, self).iterate(typeHandlers)

        playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(self.limit)
        tracksRepo = Tracks()

        featureId = self.getId('feature--valence', 'feature', 'feature--valence')
            
        for playlist in playlists:
            userId = self.getId(playlist['username'], 'user', playlist['username'], {})
            playlistId = self.getId(playlist['_id'], 'playlist', playlist['name'], playlist)
            
            yield {
                'type': 'user-playlist',
                'user': userId,
                'playlist': playlistId
            }

            # --- tracks ---
            for track in playlist['tracks']:
                trackData = tracksRepo.getTrackById(track['track_id'])
                trackId = self.getId(track['track_id'], 'track', trackData['name'], trackData)
                
                yield {
                    'type': 'playlist-track',
                    'user': userId,
                    'playlist': playlistId,
                    'track': trackId,
                    'trackData': trackData
                }

                features = tracksRepo.getFeatures(track['track_id'])
                yield {
                    'type': 'track-features',
                    'user': userId,
                    'playlist': playlistId,
                    'track': trackId,
                    'features': [
                        {
                            'id': featureId,
                            'val': features['valence']
                        }
                    ]
                }

                # --- artists ---
                artists = []
                for artist in trackData['artists']:
                    artistId = self.getId(artist['id'], 'artist', artist['name'], artist)
                    artists.append(artist['name'])

                    yield {
                        'type': 'track-artist',
                        'user': userId,
                        'playlist': playlistId,
                        'track': trackId,
                        'artist': artistId,
                        'artistData': artist
                    }
                
                # artistName = ' ++ '.join(artists)

                # --- tags ---
                if 'tags' in trackData:
                    for tag in trackData['tags']:
                        tagUid = 'tag::'+tag['name']
                        tagId = self.getId(tagUid, 'tag', tag['name'], tag)

                        yield {
                            'type': 'track-tag',
                            'user': userId,
                            'playlist': playlistId,
                            'track': trackId,
                            'trackUid': track['track_id'],
                            'tag': tagId,
                            'tagUid': tagUid,
                            'tagName': tag
                        }
