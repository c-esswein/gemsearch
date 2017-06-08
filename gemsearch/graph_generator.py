"""
Generates graph training set from mongodb
"""
from pprint import pprint
from Playlists import Playlists
from Tracks import Tracks
from Storage import Storage
import csv
import os

# TODO integrate albums

class GraphGenerator:
    pathPrefix = ''

    idCounter = 0
    lookupDict = {}

    def __init__(self, pathPrefix):
        self.pathPrefix = pathPrefix

        if not os.path.exists(pathPrefix):
            os.makedirs(pathPrefix)
        
        typeFile = open(pathPrefix + 'types.csv', 'w', encoding="utf-8")
        self.typeWriter = csv.writer(typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # get uid and write type info
    def getId(self, uidObj, type, name, uri = ""):
        uid = str(uidObj)
        if not uid in self.lookupDict:
            self.lookupDict[uid] = self.idCounter
            self.typeWriter.writerow([self.idCounter, type, uid, name, uri])
            self.idCounter += 1
        
        return str(self.lookupDict[uid])


    def get_items(self, limit):
        ''' Generator with all items in db.
        '''
        playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(limit)
        tracksRepo = Tracks()

        featureId = self.getId('feature--valence', 'feature', 'feature--valence')
            
        for playlist in playlists:
            userId = self.getId(playlist['username'], 'user', playlist['username'])
            playlistId = self.getId(playlist['_id'], 'playlist', playlist['name'])
            
            yield {
                'type': 'user-playlist',
                'user': userId,
                'playlist': playlistId
            }

            # --- tracks ---
            for track in playlist['tracks']:
                trackData = tracksRepo.getTrackById(track['track_id'])
                trackId = self.getId(track['track_id'], 'track', trackData['name'], trackData['uri'])
                
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
                    artistId = self.getId(artist['id'], 'artist', artist['name'], artist['uri'])
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
                        tagId = self.getId(tag['name'], 'tag', tag['name'])

                        yield {
                            'type': 'track-tag',
                            'user': userId,
                            'playlist': playlistId,
                            'track': trackId,
                            'tag': tagId,
                            'tagName': tag
                        }

    def write_connection(self, f, item1, item2, weight = 1):
        #print(item1, item2, weight)
        f.write(item1+' '+item2+' '+str(weight)+'\n')

    def create_biparite_graph(self, outfile, limit):
        for item in self.get_items(limit):
            if item['type'] == 'user-playlist':
                self.write_connection(outfile, item['user'], item['playlist'])
            if item['type'] == 'track-artist':
                self.write_connection(outfile, item['user'], item['artist'])
            if item['type'] == 'playlist-track':
                self.write_connection(outfile, item['user'], item['track'])
            # tags missing

    def create_normal_graph(self, outfile, limit):
        for item in self.get_items(limit):
            #print(item['type'])
            if item['type'] == 'user-playlist':
                self.write_connection(outfile, item['user'], item['playlist'])
            if item['type'] == 'track-features':
                for feature in item['features']:
                    self.write_connection(outfile, feature['id'], item['track'], feature['val'])
            if item['type'] == 'track-artist':
                self.write_connection(outfile, item['track'], item['artist'])
            if item['type'] == 'track-tag':
                self.write_connection(outfile, item['track'], item['tag'])
            if item['type'] == 'playlist-track':
                self.write_connection(outfile, item['playlist'], item['track'])

    def start_generating(self):
        with open(self.pathPrefix + 'graph.txt', 'w') as outfile:
            self.create_normal_graph(outfile, 10)

if __name__ == '__main__':
    generator = GraphGenerator('data/test1/')
    generator.start_generating()
    print("DONE: generated graph data")