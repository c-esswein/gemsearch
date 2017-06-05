from pprint import pprint
from bson.objectid import ObjectId
from Storage import Storage
from Tracks import Tracks

class Playlists:
    storage = Storage()

    def getCollection(self):
        return self.storage.getCollection('playlists')

    def getPlaylist(self, id):
        return self.storage.getCollection('playlists').find_one({"_id": id})
        
    def getPlaylistByKey(self, key):
        return self.storage.getCollection('playlists').find_one({"key": key})

    def getTrackFeatures(self, playlist):
        tracks = Tracks()
        def getTrackFeatures(track):
            if not 'track_id' in track:
                return None
            return tracks.getFeatures(track['track_id'])
        
        return list(map(lambda x: getTrackFeatures(x), playlist['tracks']))

if __name__ == '__main__':
    playlists = Playlists()
    playlist = playlists.getPlaylistByKey('64702d99ca4e1596756d1cacbc492d0d_ â–º')
    # pprint(playlist)
    
    tracks = playlists.getTrackFeatures(playlist)
    pprint(tracks)
