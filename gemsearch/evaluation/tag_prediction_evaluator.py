from pprint import pprint
import numpy as np
from sklearn.model_selection import train_test_split


''' hides tags for tracks during training and evaluates
track tag prediction
'''
class TagPredictionEvaluator:

    name = 'Tag Prediction Evaluator'
    _testTags = []

    def __init__(self, testSplit = 0.2, precisionAt = 5):
        self._testSplit = testSplit
        self._precisionAt = precisionAt

    def traverse(self, tagTraverser):
        tags = list(tagTraverser)
        training, test = train_test_split(tags, test_size=self._testSplit, random_state=42)
        self._testTags = test

        return training

    def evaluate(self, geCalc):
        hits = 0

        for track, tag, weight in self._testTags:
            if evaluate_track_tag_predict(geCalc, self._precisionAt, track['id'], tag['id']):
                print('Hit Tag: {}'.format(tag['id']))
                hits += 1
            else:
                #print('Missed Tag: {}'.format(tagData['name']))
                pass
        
        tagCount = len(self._testTags)
        print('Evaluator {}, split={}, tagCount={}'.format(self.name, self._testSplit, tagCount))
        print('Hit Rate: {}'.format(hits / tagCount))


# ------------- static functions ------------

def evaluate_track_tag_predict(geCalc, precisionAt, track, tag):
    '''Evaluates tag prediction for track
    '''
    
    results = geCalc.query_by_ids(
        [track], 
        typeFilter = ['tag'], 
        limit = precisionAt
    )
    
    for recTag in results:
        if recTag['id'] == tag:
            return True

    return False
