from pprint import pprint
import numpy as np

from gemsearch.query.elastic_search import extract_query_from_name

''' is a evaluator and typeHandler
'''
class PlaylistQueryEvaluator:

    name = 'Playlist Query Evaluator'
    playlists = []
    testRatio = 0.2

    def addItem(self, idCounter, uidObj, type, name, obj = {}):
        if type == 'playlist':
            self.playlists.append(obj)

    def close_type_handler(self):
        pass

    def evaluate(self, geCalc):
        # select random test playlists
        playlistCount = max(1, int(len(self.playlists) * self.testRatio))
        randomPlaylists = np.random.choice(self.playlists, playlistCount)

        totalScore = 0
        for playlist in randomPlaylists:
            score = evaluate_playlist(geCalc, playlist)
            totalScore = totalScore + score
            print('Playlist: '+str(score)+' <<'+playlist['name']+'>>')
        
        print('Avg score: '+str(totalScore/playlistCount)+' @ '+str(playlistCount)+' Playlists')

# ------------- static functions ------------

def evaluate_playlist(geCalc, playlist):
    '''Evaluates playlist name as query performance.
    '''
    queryIds = extract_query_from_name(playlist['name'])
    playlistCount = len(playlist['tracks'])
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = playlistCount * 2
    )

    numHits = match_track_hits(playlist['tracks'], results)
    return numHits / playlistCount

def match_track_hits(playlistTracks, recTracks):
    hits = 0
    for track in playlistTracks:
        trackId = str(track['track_id'])
        for recTrack in recTracks:
            if recTrack['id'] == trackId:
                hits += 1
                break

    return hits

if __name__ == '__main__':
    from gemsearch.storage.Storage import Storage
    from gemsearch.embedding.ge_calc import GeCalc

    playlists = Storage().getCollection('tmp_playlists_cleaned').find({}, no_cursor_timeout=True).limit(2)
    geCalc = GeCalc('data/tmp_test/')

    evaluator = PlaylistQueryEvaluator()

    for playlist in playlists:
        evaluator.addItem('idCounter', 'uidObj', 'playlist', 'name', playlist)
    
    evaluator.evaluate(geCalc)
