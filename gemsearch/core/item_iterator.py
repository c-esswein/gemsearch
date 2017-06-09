"""Iterates over all items in db
"""

from gemsearch.storage.Storage import Storage
from gemsearch.storage.Tracks import Tracks

# TODO integrate albums

class ItemIterator:
    typeHandlers = []
    idCounter = 0
    lookupDict = {}
    limit = 0

    def __init__(self, limit = 10):
        self.limit = limit

    def getId(self, uidObj, type, name, obj = {}):
        '''Returns unique int identifier
        '''
        uid = str(uidObj)
        if not uid in self.lookupDict:
            self.lookupDict[uid] = self.idCounter
            self.newItemId(self.idCounter, uid, type, name, obj)
            self.idCounter += 1
        
        return str(self.lookupDict[uid])
    
    def newItemId(self, idCounter, uidObj, type, name, obj = {}):
        '''called when new item is iterated
        '''
        for typeHandler in self.typeHandlers:
            typeHandler.addItem(idCounter, uidObj, type, name, obj)

    def iterate(self, typeHandlers):
        ''' Generator with all items in db.
        '''
        self.typeHandlers = typeHandlers

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
                        tagId = self.getId('tag::'+tag['name'], 'tag', tag['name'], tag)

                        yield {
                            'type': 'track-tag',
                            'user': userId,
                            'playlist': playlistId,
                            'track': trackId,
                            'tag': tagId,
                            'tagName': tag
                        }
