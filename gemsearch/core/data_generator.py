'''Loads data from mongodb and creates data files.

In this step playlist names and tag names are cleaned.abs
'''

import json
import csv
from gemsearch.core.abstract_data_generator import ADataGenerator
from gemsearch.storage.Storage import Storage
from gemsearch.storage.Tracks import Tracks
from gemsearch.core.name_cleaning import clean_playlist_name, clean_tag


# TODO integrate albums

class DataGenerator(ADataGenerator):

    def writePlaylists(self, limit):
        ''' Exports playlists and contained tracks.
        '''
        playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(limit)
        
        # --- playlist ---
        counter = 0
        for playlist in playlists:

            # print progress
            counter += 1
            if counter % 100 == 0:
                print('written {}/{}'.format(counter, limit))

            # clean playlist name
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
                self.writeTrack(None, track['track_uri'])

    def writeUsers(self, limit):
        ''' Exports all users and contained tracks.
        '''
        users = Storage().getCollection('users').find({}, no_cursor_timeout=True).limit(limit)
        for user in users:
            self.writeUser(user)

    def writeUser(self, user):
        ''' Exports given user with tracks
        '''

        # --- tracks ---
        for track in user['tracks']:
            self.write('user_tracks', [
                user['id'],
                track['track_uri']
            ])

            self.writeTrack(None, track['track_uri'])


    def writeTrack(self, track = None, trackUri = None):
        ''' Exports track with tags and artists. 
        Provide either db track entry or only db track id.
        '''
        trackId = trackUri or track['uri']

        if self.checkIfWritten(trackId):
            return

        # load track if only id is given
        if track is None:
            tracksRepo = Tracks()
            track = tracksRepo.getTrack(trackUri)

        if track is None:
            raise Exception('Precondition violation: track is null')


        # --- features ---
        features = tracksRepo.getFeatures(track['_id'])
        if features:
            self.writeJson('track_features', {
                'id': trackId,
                'name': track['name'],
                'features': {
                    'valence': features['valence']
                }
            })
        else:
            print('missing feature for track: ' + str(trackId))
            # TODO dummy feature...
            self.writeJson('track_features', {
                'id': trackId,
                'name': track['name'],
                'features': {
                    'valence': 1
                }
            })
        
        # --- artists ---
        for artist in track['artists']:
            artistId = artist['id']

            self.write('track_artist', [
                trackId,
                artist['uri'],
                artist['name']
            ])

            self.writeArtist(artist)

        # --- tags ---
        if 'tags' in track:
            for tag in track['tags']:
                # clean tag name                
                tagName = clean_tag(tag)
                if tagName:
                    self.write('track_tag', [
                        trackId,
                        tagName
                    ])

    def writeArtist(self, artist):
        ''' Exports artist with genres.
        '''

        artistId = artist['id']

        if self.checkIfWritten(artistId):
            return

        # TODO write artist genres        


if __name__ == "__main__":
    generator = DataGenerator('data/tmp/')
    generator.writePlaylists(2)
    #generator.writeUsers(5)
    generator.closeHandlers()
    print('data written')
