from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
from pprint import pprint
from sklearn.model_selection import train_test_split
import pickle


''' hides tags for tracks during training and evaluates
track tag prediction
'''
class TagPredictionEvaluator:

    name = 'Tag Prediction Evaluator'
        
    def __init__(self):
        self._testTags = []

    def __init__(self, testSplit = 0.2, topNAccuracy = [5]):
        self._testSplit = testSplit
        self._topNAccuracy = topNAccuracy

    def traverse(self, tagTraverser):
        tags = list(tagTraverser)
        training, test = train_test_split(tags, test_size=self._testSplit, random_state=42)
        self._testTags = test

        logger.info('splitted trainingsdata: training %s, test %s tags', len(training), len(test))

        # write test data to file in case of process termination
        pickle.dump(test, open('tag_predict_test.p', 'wb'))

        return training
    
    def loadIntermediateTags(self):
        self._testTags = pickle.load(open('tag_predict_test.p', 'rb'))

    def evaluate(self, geCalc):
        tagCount = len(self._testTags)

        raise Exception('not implemented')

        logger.info('started tag prediction evaluator with %s test tags', tagCount)

        if (tagCount < 1):
            logger.error('No test tags set for evaluation')
            return
        
        # build track - tag relation
        trackTags = {} # Map<TrackId, TagIds[]>
        for track, tag, weight in self._testTags:
            if not (track['id'] in trackTags):
                trackTags[track['id']] = []
            
            trackTags[track['id']].append(tag['id'])
        
        maxTopNAccuracy = max(self._topNAccuracy)
        for trackId in trackTags:
            pass
            # TODO: ....


        for topNAccuracy in range(1, self._topNAccuracy + 1):
            logger.info('\n--- top %s accuracy ---', topNAccuracy)
            hits = 0
            randomHits = 0
            for track, tag, weight in self._testTags:
                if evaluate_track_tag_predict(geCalc, topNAccuracy, track['id'], tag['id']):
                    hits += 1
                if evaluate_track_tag_predict(geCalc, topNAccuracy, track['id'], tag['id'], randomGuess = True):
                    randomHits += 1
            
            logger.info('Avg: top %s accuracy: %s (random: %s) @ %s tags (testsplit=%s)',
                topNAccuracy,
                hits / tagCount,
                randomHits / tagCount,
                tagCount,
                self._testSplit
            )

# ------------- static functions ------------

def evaluate_track_tag_predict(geCalc, topNAccuracy, track, tag, randomGuess = False):
    '''Evaluates tag prediction for track
    '''
    
    if randomGuess:
        results = geCalc.random_query_results(
            typeFilter = ['tag'], 
            limit = topNAccuracy
        )
    else:
        results = geCalc.query_by_ids(
            [track], 
            typeFilter = ['tag'], 
            limit = topNAccuracy
        )


    # check if tag is in recommended tags
    return any((recTag['id'] == tag) for recTag in results)



def checkMatchesAt(recResult, test, firstN):
    ''' Count matches of test in recResult within first n elements
    '''
    hits = 0
    for i in range(0, firstN):
        if recResult[i]['id'] in test:
            hits += 1

    return hits
