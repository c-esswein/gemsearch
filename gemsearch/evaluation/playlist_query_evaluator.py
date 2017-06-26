from pprint import pprint
import numpy as np
import random
import json

from gemsearch.query.elastic_search import extract_query_from_name
from gemsearch.utils.JSONEncoder import JSONEncoder

''' is a evaluator and typeHandler
'''
class PlaylistQueryEvaluator:

    name = 'Playlist Query Evaluator'
    _playlists = []
    _testSplit = 0.2

    def __init__(self, testSplit = 0.2):
        self._testSplit = testSplit
    
    def traverse(self, playlistTraverser):
        playlists = list(playlistTraverser)
        training, test = train_test_split(playlists, test_size=self._testSplit, random_state=42)
        self._playlists = test

        return training
    
    def addPlaylists(self, playlistTraverser):
        self._playlists = list(playlistTraverser)

    # TODO: remove?
    def writeTestLists(self, dataDir):
        # write chosen playlists into file for easier testing
        with open(dataDir+'playlist_evaluation.json', 'w', encoding="utf-8") as outFile:
            for playlist in self._playlists:
                outFile.write(json.dumps(playlist, cls=JSONEncoder) + '\n')

    def evaluate(self, geCalc):
        playlistCount = len(self._playlists)

        if playlistCount < 1:
            raise Exception('No Playlists collected to test!')

        totalScore = 0
        for playlist in self.playlists:
            score = evaluate_playlist(geCalc, playlist)
            totalScore = totalScore + score
            print('Playlist: '+str(score)+' <<'+playlist['name']+'>>')
        
        print('Avg score: '+str(totalScore/playlistCount)+' @ '+str(playlistCount)+' Playlists')

# ------------- static functions ------------

def evaluate_playlist(geCalc, playlist):
    '''Evaluates playlist name as query performance.
    '''
    queryIds = extract_query_from_name(playlist['playlistName'])
    playlistCount = len(playlist['tracks'])
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = playlistCount * 2 # TODO: put into parameter, use precision / recall
    )

    numHits = match_track_hits(playlist['tracks'], results)
    return numHits / playlistCount

def match_track_hits(playlistTracks, recTracks):
    hits = 0
    for trackId in playlistTracks:
        for recTrack in recTracks:
            if recTrack['id'] == trackId:
                hits += 1
                break

    return hits

if __name__ == '__main__':
    from gemsearch.storage.Storage import Storage
    from gemsearch.embedding.ge_calc import GeCalc, read_type_file

    dataFolder = 'data/tmp1/'

    playlistsCol = Storage().getCollection('playlists')
    playlists = playlists.find({}).limit(1000)

    evaluator = PlaylistQueryEvaluator()

    for playlist in playlists:
        # TODO: outdated api
        evaluator.addItem('idCounter', 'uidObj', 'playlist', 'name', playlist)
    
    geCalc = GeCalc()
    geCalc.load_node2vec_data(dataFolder+'embedding.em', dataFolder+'types.csv')
    evaluator.evaluate(geCalc)
