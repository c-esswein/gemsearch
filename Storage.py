from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

class Storage:
    DB_NAME = "dbis"
    client = MongoClient()
    db = client.get_database(DB_NAME)

    def getCollection(self, collectionName):
        return self.db[collectionName];

    def getTrack(self, trackUri):
        return self.getCollection('tracks').find({"uri": trackUri})

    def getFeatures(self, track):
        pprint(ObjectId(track['_id']))
        audios = self.getCollection('audios').find({'track_id': ObjectId(track['_id'])})
        return audios[0]

if __name__ == '__main__':
    storage = Storage()
    track = storage.getTrack('spotify:track:06ngjaiEea4jvIcAIcxcGr')
    pprint(track[0])
    print("----FEATURES----")
    pprint(storage.getFeatures(track[0]))
