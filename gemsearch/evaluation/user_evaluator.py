from pprint import pprint
import numpy as np
import random
import pickle
import json
from sklearn.model_selection import train_test_split 
import logging
logger = logging.getLogger(__name__)

from gemsearch.query.elastic_search import extract_query_from_name
from gemsearch.utils.JSONEncoder import JSONEncoder

''' Evaluates classic collaborative filtering:
- take all playlists
- build user - track map
- split training: top 0.8 tracks per user (filter users having n < threshold tracks)

- embed training data

- per user
    - get test * precision@k tracks
    - check precision
- accumulate
'''
class UserEvaluator:

    name = 'User Evaluator'
    _users = {}
    _testSplit = 0
    _maxPrecisionAt = 0
    _minTracksPerUser = 0

    def __init__(self, testSplit = 0.2, maxPrecisionAt = 1, minTracksPerUser = 10):
        self._testSplit = testSplit
        self._maxPrecisionAt = maxPrecisionAt
        self._minTracksPerUser = minTracksPerUser
    
    def addUserTracks(self, userTracksTraverser):
        '''Add user-tracks to evaluator. Test split is applied per user and Training data
        is returned.
        '''
        
        # load complete data
        users = {}
        for (user, track, weight) in userTracksTraverser:
            userId = user['id']
            if not (userId in users):
                users[userId] = []

            users[userId].append((user, track, weight))

        # split per user
        training = []
        for userId in users:
            userTracks = users[userId]

            # skip users without enough tracks
            if len(userTracks) < self._minTracksPerUser:
                continue
            
            # split
            userTraining, test = train_test_split(userTracks, test_size=self._testSplit, random_state=42)
            training.extend(userTraining)
            
            # only store track ids (smaller footprints)
            self._users[userId] = (
                [track['id'] for (user, track, weight) in userTraining], 
                [track['id'] for (user, track, weight) in test]
            )
        
        logger.info('Generated test data for %s users (discarded %s). User-Track training count: %s', 
            len(self._users), len(users) - len(self._users), len(training)
        )

        return training

    
    def writeTestData(self, dataPath):
        '''Writes splitted test data to dataDir.
        '''
        pickle.dump(self._users, open(dataPath, 'wb'))

    def loadTestData(self, dataPath):
        '''Read stored splitted test data.
        '''
        self._users = pickle.load(open(dataPath, 'rb'))
    

    def evaluate(self, geCalc):
        '''Starts evaluation.
        '''
        userCount = len(self._users)
        logger.info('Started user evaluation with %s users', userCount)

        if userCount < 1:
            raise Exception('Precondition violation: No users collected to test!')

        # functions to calculate recommendations
        recFunctions = [getRecommenderTracks, getRandomTracks]
        
        # init stats counter
        stats = {}

        # evaluate per user
        for userId in self._users:
            (training, test) = self._users[userId]

            for recFunction in recFunctions:
                self.evalUser(userId, training, test, geCalc, recFunction, stats)
        
        logger.info('Finished user eval, results:')
        for methodName in stats:
            # calculate result stats
            stats[methodName]['precision'] /= userCount
            stats[methodName]['recall'] /= userCount

            logger.info('method %s: precision: %s, recall %s', 
                methodName, stats[methodName]['precision'], stats[methodName]['recall']
            )

        return stats

    def evalUser(self, userId, training, test, geCalc, recFunction, stats):
        ''' Evaluates training test set with given geCalc. Result is stored in stats obj.
        '''
        testLen = len(test)     
        
        # get recommendation tracks
        limit = len(training) + (self._maxPrecisionAt * testLen)
        recResult = recFunction(geCalc, userId, limit)
        
        # remove training tracks
        recResult = [track for track in recResult \
                        if not track in training]

        # calculate matches per precision@k
        for precisionAt in range(1, self._maxPrecisionAt + 1):
            matches = checkMatchesAt(recResult, test, precisionAt * testLen)

            methodName = recFunction.__name__ + ' @' + str(precisionAt)
            # init stats
            if not methodName in stats:
                stats[methodName] = {
                    'precision': 0,
                    'recall': 0
                }

            stats[methodName]['precision'] += matches / (precisionAt * testLen)
            stats[methodName]['recall'] += matches / testLen

# ------------- static functions ------------

def getRecommenderTracks(geCalc, user, limit):
    return geCalc.query_by_ids(
        [user], 
        typeFilter = ['track'], 
        limit = limit
    )


def getRandomTracks(geCalc, user, limit):
    return geCalc.random_query_results(
        typeFilter = ['track'], 
        limit = limit
    )


def checkMatchesAt(recResult, test, firstN):
    ''' Count matches of test in recResult within first n elements
    '''
    hits = 0
    for i in range(0, firstN):
        if recResult[i]['id'] in test:
            hits += 1

    return hits
