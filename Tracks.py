from pprint import pprint
from bson.objectid import ObjectId
from Storage import Storage

class Tracks:
    storage = Storage()

    def getTrack(self, trackUri):
        return self.storage.getCollection('tracks').find_one({"uri": trackUri})

    def getFeatures(self, trackId):
        audios = self.storage.getCollection('audios').find_one({'track_id': ObjectId(trackId)})
        return audios

if __name__ == '__main__':
    tracks = Tracks()
    track = tracks.getTrack('spotify:track:06ngjaiEea4jvIcAIcxcGr')
    pprint(track)
    print("----FEATURES----")
    pprint(tracks.getFeatures(track['_id']))
