from pprint import pprint
import numpy as np
import random
import json
from sklearn.model_selection import train_test_split 
import logging
logger = logging.getLogger(__name__)

from gemsearch.query.elastic_search import extract_query_from_name, extract_multiple_queries_from_name
from gemsearch.utils.JSONEncoder import JSONEncoder

''' Evaluates playlist name -> query matching.abs
Collects playlists, takes random test split and tries to extract query from playlist name.
'''
class PlaylistQueryEvaluator:

    name = 'Playlist Query Evaluator'
    _playlists = []
    _testSplit = 0
    _maxPrecisionAt = 0
    _hasExtractedQueries = False

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

    def writeTestLists(self, filePath):
        '''write chosen playlists into file for easier testing
        '''
        with open(filePath, 'w', encoding="utf-8") as outFile:
            for playlist in self._playlists:
                outFile.write(json.dumps(playlist, cls=JSONEncoder) + '\n')

    def loadTestLists(self, filePath):
        '''read stored test playlists as test lists.
        '''
        with open(filePath, 'r', encoding="utf-8") as inFile:
            for line in inFile:
                playlist = json.loads(line)
                self._playlists.append(playlist)

    def extractQueries(self):
        ''' Extracts and stores queries from playlist names
        '''
        logger.info('Extract queries from playlist names (result is cached)')
        
        extractedPlaylists = []
        for playlist in self._playlists:
            
            # extract and store queries
            playlist['extracted_queries'] = {
                'simple_first_match': extract_query_from_name(playlist['playlistName'], 1),
                'simple_first_two_match': extract_query_from_name(playlist['playlistName'], 2),
                'multiple_queries': extract_multiple_queries_from_name(playlist['playlistName'], 1)
            }
                
            # check if any extraction has returned results
            hasQuery = np.any([len(playlist['extracted_queries'][extractName]) > 0 for extractName in playlist['extracted_queries']])
            if not hasQuery:
                # no query could be extracted
                logger.debug('no query possible for playlist %s', playlist['playlistName'])
                continue
            
            logger.debug('query for name: %s %s', playlist['playlistName'], playlist['extracted_queries'])

            extractedPlaylists.append(playlist)

        logger.info('For evaluation %s of %s playlists are left', len(extractedPlaylists), len(self._playlists))        

        self._playlists = extractedPlaylists
        self._hasExtractedQueries = True

        return extractedPlaylists

    def evaluate(self, geCalc):
        '''Starts evaluation.
        '''
        playlistCount = len(self._playlists)
        logger.info('Started playlist evaluation with %s playlists', playlistCount)

        if playlistCount < 1:
            raise Exception('No Playlists collected to test!')

        if not self._hasExtractedQueries:
            self.extractQueries()
        
        # evaluation functions to run for every playlist
        evaluationFuncs = [rec_random_tracks, rec_query_tracks, rec_first_two_query_tracks]
        if self._useUserContext:
            evaluationFuncs.append(rec_query_tracks_with_user)
            evaluationFuncs.append(rec_tracks_with_user)

        # init metrics
        noQueryPossible = 0
        stats = {}

        for playlist in self._playlists:
        
            for evalFunc in evaluationFuncs:

                # execute and store performance
                playlistTrackCount = len(playlist['tracks'])
                limit = max(playlistTrackCount, self._maxPrecisionAt)
                recItems = evalFunc(geCalc, playlist, limit)

                for precisionAt in range(1, self._maxPrecisionAt + 1):        
                    statName = evalFunc.__name__ + '@' + str(precisionAt)

                    # init stats entry
                    if not statName in stats:
                        stats[statName] = {
                            'precision': 0,
                            'precision_on_has_hits': 0,
                            'recall': 0,
                            'avg_hits': 0,
                            'avg_hits_on_has_hits': 0,
                            'has_hits': 0,
                        }
                    
                    hits = checkMatchesAt(recItems, playlist['tracks'], precisionAt)
                    
                    stats[statName]['precision'] += hits / precisionAt
                    stats[statName]['recall'] += hits / playlistTrackCount
                    stats[statName]['avg_hits'] += hits

                    if hits > 0:
                        stats[statName]['precision_on_has_hits'] += hits / precisionAt
                        stats[statName]['has_hits'] += 1
                        stats[statName]['avg_hits_on_has_hits'] += hits  
    
        
        # calculate average:
        for statName in stats:
            stats[statName]['precision'] /= playlistCount
            stats[statName]['recall'] /= playlistCount
            stats[statName]['avg_hits'] /= playlistCount
            if stats[statName]['has_hits'] > 0:
                stats[statName]['precision_on_has_hits'] /= stats[statName]['has_hits']
                stats[statName]['avg_hits_on_has_hits'] /= stats[statName]['has_hits']
            else:
                stats[statName]['precision_on_has_hits'] = 0
                stats[statName]['avg_hits_on_has_hits'] = 0

        logger.info('Playlist evaluation finished: total %s playlists (testsplit=%s), no query extracted for %s', playlistCount, self._testSplit, noQueryPossible)
        for statName in sorted(stats.keys()):
            logger.info('___ method: %s', statName)
            for metric in stats[statName]:
                logger.info('%s: %s', metric, stats[statName][metric])

        return stats

# ------------- static functions ------------

def rec_query_tracks_with_user(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match']    
    queryIds.append(playlist['userId'])
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_tracks_with_user(geCalc, playlist, limit):
    ''' Uses user context alone to rec tracks (query is not included!).
    '''
    queryIds = [playlist['userId']]
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_first_two_query_tracks(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    queryIds = playlist['extracted_queries']['simple_first_two_match']
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_query_tracks(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match']
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_random_tracks(geCalc, playlist, limit):
    ''' Uses random recommender to predict playlist tracks.
    '''    
    results = geCalc.random_query_results(
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def checkMatchesAt(recResult, testTracks, firstN):
    ''' Counts matches of test in recResult within first n elements
    '''
    hits = 0
    for i in range(0, firstN):
        if recResult[i]['id'] in testTracks:
            hits += 1

    return hits
