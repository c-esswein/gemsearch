''''Loads data from mongodb and creates data files.
'''
import json
import csv
import re
from gemsearch.storage.Storage import Storage
from gemsearch.storage.Tracks import Tracks
from gemsearch.core.name_cleaning import clean_playlist_name, clean_tag


# TODO integrate albums

class DataGenerator():

    _idWritten = {}
    _handlers = {}

    def __init__(self, dataDir):
        self._dataDir = dataDir

    def _getHandler(self, fileName):
        if fileName not in self._handlers:
            self._handlers[fileName] = open(fileName, 'w', encoding="utf-8")

        return self._handlers[fileName]

    def _closeHandlers(self):
        for handler in self._handlers:
            self._handlers[handler].close()

    def write(self, connectionName, data):
        fileName = self._dataDir + connectionName + '.csv'
        # todo lazy init, close on ending
        outputFile = self._getHandler(fileName)
        csvWriter = csv.writer(outputFile, delimiter=',', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(data)

    def writeJson(self, connectionName, data):
        fileName = self._dataDir + connectionName + '.json'
        outputFile = self._getHandler(fileName)
        outputFile.write(json.dumps(data) + '\n')

    def generate(self, limit):
        playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(limit)
        tracksRepo = Tracks()

        # --- playlist ---
        for playlist in playlists:

            playlistName = clean_playlist_name(playlist['name'])
            if not playlistName:
                continue

            self.write('playlist', [
                playlist['_id'],
                playlist['username'],
                playlistName,
                [track['track_uri'] for track in playlist['tracks']]
            ])

            # --- tracks ---
            for track in playlist['tracks']:
                trackId = track['track_uri']
                if trackId in self._idWritten:
                    continue
                else:
                    self._idWritten[trackId] = True

                # --- features ---
                trackData = tracksRepo.getTrackById(track['track_id'])
                features = tracksRepo.getFeatures(track['track_id'])
                
                self.writeJson('track_features', {
                    'id': trackId,
                    'name': trackData['name'],
                    'features': {
                        'valence': features['valence']
                    }
                })
                
                # --- artists ---
                for artist in trackData['artists']:
                    artistId = artist['id']

                    self.write('track_artist', [
                        trackId,
                        artist['uri'],
                        artist['name']
                    ])

                    '''
                    if artistId is in self._idWritten:
                        continue
                    else:
                        self._idWritten[artistId] = True
                    
                    # TODO write artist genres
                    '''
                

                # --- tags ---
                if 'tags' in trackData:
                    for tag in trackData['tags']:
                        tagName = clean_tag(tag)
                        if tagName:
                            self.write('track_tag', [
                                trackId,
                                tagName
                            ])

        self._closeHandlers()

if __name__ == "__main__":
    generator = DataGenerator('data/graph_100/')
    generator.generate(100)
    print('data written')
