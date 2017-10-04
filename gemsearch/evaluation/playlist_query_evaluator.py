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
    
    def traverseAndSplitPlaylists(self, playlistTraverser):
        '''Add playlists to test on. testSplit is randomly applied to generate subsets 
        for training and testing.
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

    def loadTestLists(self, dataDir):
        '''read stored test playlists as test lists.
        '''
        with open(dataDir+'playlist_evaluation.json', 'r', encoding="utf-8") as inFile:
            for line in inFile:
                playlist = json.loads(line)
                self._playlists.append(playlist)

    def evaluate(self, geCalc):
        '''Starts evaluation.
        '''
        playlistCount = len(self._playlists)
        logger.info('Started playlist evaluation with %s playlists', playlistCount)

        if playlistCount < 1:
            raise Exception('No Playlists collected to test!')
        
        # functions to run for every playlist
        evaluationFuncs = [evaluate_playlist, evaluate_random_guess]

        # init metrics
        noQueryPossible = 0
        stats = {}

        for playlist in self._playlists:        

            # extract query
            queryIds = extract_query_from_name(playlist['playlistName'])
            if self._useUserContext:
                queryIds.append(playlist['userId'])
            
            # no query could be extracted
            if len(queryIds) < 1:
                noQueryPossible += 1
                continue
        
            for precisionAt in range(1, self._maxPrecisionAt + 1):        
                for evalFunc in evaluationFuncs:
                    statName = evalFunc.__name__ + '@' + str(precisionAt)
                    # init metric entry
                    if not statName in stats:
                        stats[statName] = {
                            'precision': 0,
                            'recall': 0,
                        }

                    # execute and store performance
                    recall, precision = evalFunc(geCalc, playlist, queryIds, precisionAt)
                    stats[statName]['precision'] = stats[statName]['precision'] + precision
                    stats[statName]['recall'] = stats[statName]['recall'] + recall
    
        
        # calculate average:
        for statName in stats:
            stats[statName]['precision'] = stats[statName]['precision'] / playlistCount
            stats[statName]['recall'] = stats[statName]['recall'] / playlistCount

        logger.info('Playlist evaluation finished: total %s playlists (testsplit=%s), no query extracted for %s', playlistCount, self._testSplit, noQueryPossible)
        for statName in stats:
            logger.info('Playlist evaluation result: %s -> precision %s, recall %s', statName, stats[statName]['precision'], stats[statName]['recall'])

        return stats

# ------------- static functions ------------

def evaluate_playlist(geCalc, playlist, queryIds, precisionAt = 1):
    '''Evaluates playlist name as query performance.
    '''

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

def evaluate_random_guess(geCalc, playlist, queryIds, precisionAt = 1):
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
