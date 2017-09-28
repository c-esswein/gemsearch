from pprint import pprint
import numpy as np
import random
import json
from sklearn.model_selection import train_test_split 
import logging
logger = logging.getLogger(__name__)

from gemsearch.query.elastic_search import extract_query_from_name
from gemsearch.utils.JSONEncoder import JSONEncoder

''' Evaluates playlist name -> query matching.abs
Collects playlists, takes random test split and tries to extract query from playlist name.
'''
class PlaylistQueryEvaluator:

    name = 'Playlist Query Evaluator'
    _playlists = []
    _testSplit = 0
    _maxPrecisionAt = 0

    def __init__(self, testSplit = 0.2, maxPrecisionAt = 1, useUserContext = False):
        self._testSplit = testSplit
        self._maxPrecisionAt = maxPrecisionAt
        self._useUserContext = useUserContext
    
    def traverse(self, playlistTraverser):
        '''Add playlists to test on. testSplit is randomly applied to generate subset.
        '''
        playlists = list(playlistTraverser)
        training, test = train_test_split(playlists, test_size=self._testSplit, random_state=42)

        # make sure all test users are present in training set
        usersInTraining = {}
        for trainingPlaylist in training:
            usersInTraining[trainingPlaylist['userId']] = True

        self._playlists = [x for x in test if (x['userId'] in usersInTraining)]

        logger.info('Splitted playlists for training (%s) and test (%s), total (%s)', len(training), len(self._playlists), len(playlists))

        return training
    
    def addPlaylists(self, playlistTraverser):
        '''Manually add playlists to test on.
        '''
        self._playlists = list(playlistTraverser)

    def writeTestLists(self, dataDir):
        '''write chosen playlists into file for easier testing
        '''
        with open(dataDir+'playlist_evaluation.json', 'w', encoding="utf-8") as outFile:
            for playlist in self._playlists:
                outFile.write(json.dumps(playlist, cls=JSONEncoder) + '\n')

    def evaluate(self, geCalc):
        '''Starts evaluation.
        '''
        playlistCount = len(self._playlists)
        logger.info('Started playlist evaluation with %s playlists', playlistCount)

        if playlistCount < 1:
            raise Exception('No Playlists collected to test!')
        
        for precisionAt in range(1, self._maxPrecisionAt + 1):
            logger.info('--- Precision@%s ---', precisionAt)

            self.runEvaluation(evaluate_playlist, geCalc, precisionAt, self._useUserContext)
            self.runEvaluation(evaluate_random_guess, geCalc, precisionAt, self._useUserContext)
    
    def runEvaluation(self, evaluationFunc, geCalc, precisionAt, useUserContext):
        ''' Starts evaluation with given evaluation method and logs results.
        '''
        totalRecall = 0
        totalPrecision = 0
        for playlist in self._playlists:
            recall, precision = evaluationFunc(geCalc, playlist, precisionAt, useUserContext)
            totalRecall = totalRecall + recall
            totalPrecision = totalPrecision + precision
        
        playlistCount = len(self._playlists)        
        logger.info('Avg: precision@%s: %s, recall %s @ %s playlists (testsplit=%s) method: %s',
            precisionAt,
            totalPrecision / playlistCount,
            totalRecall / playlistCount,
            playlistCount,
            self._testSplit,
            evaluationFunc.__name__
        )

# ------------- static functions ------------

def evaluate_playlist(geCalc, playlist, precisionAt = 1, useUserContext = False):
    '''Evaluates playlist name as query performance.
    '''
    queryIds = extract_query_from_name(playlist['playlistName'])
    if len(queryIds) < 1:
        return (0, 0)

    if useUserContext:
        queryIds.append(playlist['userId'])

    playlistCount = len(playlist['tracks'])
    limit = playlistCount * precisionAt
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )

    numHits = match_track_hits(playlist['tracks'], results)
    if numHits > 0:
        logger.debug('Playlist: precision %s <<%s>> query:[%s]',
            numHits / limit,
            playlist['playlistName'],
            queryIds[0]
        )

    return (
        numHits / playlistCount, # recall
        numHits / limit, # precision
    )

def evaluate_random_guess(geCalc, playlist, precisionAt = 1, useUserContext = False):
    '''Evaluates playlist name as query performance (results are rando entries).
    '''
    
    playlistCount = len(playlist['tracks'])
    limit = playlistCount * precisionAt
    results = geCalc.random_query_results(
        typeFilter = ['track'], 
        limit = limit
    )

    numHits = match_track_hits(playlist['tracks'], results)

    return (
        numHits / playlistCount, # recall
        numHits / limit, # precision
    )

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
