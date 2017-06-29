from pprint import pprint
from sklearn.model_selection import train_test_split


''' hides tags for tracks during training and evaluates
track tag prediction
'''
class TagPredictionEvaluator:

    name = 'Tag Prediction Evaluator'
    _testTags = []

    def __init__(self, testSplit = 0.2, maxTopNAccuracy = 5):
        self._testSplit = testSplit
        self._maxTopNAccuracy = maxTopNAccuracy

    def traverse(self, tagTraverser):
        tags = list(tagTraverser)
        training, test = train_test_split(tags, test_size=self._testSplit, random_state=42)
        self._testTags = test

        return training

    def evaluate(self, geCalc):
        tagCount = len(self._testTags)

        for topNAccuracy in range(1, self._maxTopNAccuracy + 1):
            print('\n--- top {} accuracy ---'.format(topNAccuracy))
            hits = 0
            for track, tag, weight in self._testTags:
                if evaluate_track_tag_predict(geCalc, topNAccuracy, track['id'], tag['id']):
                    print('Hit Tag: {}'.format(tag['id']))
                    hits += 1
            
            print('Avg: top {} accuracy: {} @ {} tags (testsplit={})'.format(
                topNAccuracy,
                hits / tagCount,
                tagCount,
                self._testSplit
            ))

# ------------- static functions ------------

def evaluate_track_tag_predict(geCalc, topNAccuracy, track, tag):
    '''Evaluates tag prediction for track
    '''
    
    results = geCalc.query_by_ids(
        [track], 
        typeFilter = ['tag'], 
        limit = topNAccuracy
    )
    
    # check if tag is in recommended tags
    return any((recTag['id'] == tag) for recTag in results)
