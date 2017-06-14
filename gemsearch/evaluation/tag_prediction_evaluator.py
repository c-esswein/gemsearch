from pprint import pprint
import numpy as np

from gemsearch.query.elastic_search import extract_query_from_name

''' hides tags for tracks during training and evaluates
track tag prediction
'''
class TagPredictionEvaluator:

    name = 'Tag Prediction Evaluator'
    tags = {}
    firstNTags = 0
    precisionAt = 1
    testTags = None

    def __init__(self, precisionAt = 5, firstNTags = 0, testTags = None):
        self.precisionAt = precisionAt
        self.firstNTags = firstNTags
        self.testTags = testTags

    def addItem(self, idCounter, uidObj, type, name, obj = {}):
        if type != 'tag':
            return

        addTag = False

        if (self.testTags is not None) and (name in self.testTags): # tagList mode
            addTag = True
        elif (self.firstNTags > 0): # take first N tags mode
            addTag = True
            self.firstNTags -= 1

        if addTag:
            self.tags[uidObj] = {
                'name': name,
                'track': None
            }

    def close_type_handler(self):
        pass

    def generateItem(self, item):
        if item['type'] == 'track-tag':
            tagKey = item['tagUid']
            if tagKey in self.tags and self.tags[tagKey]['track'] == None:
                self.tags[tagKey]['track'] = str(item['trackUid'])
                return True

        return False

    def close_generation(self):
        pass

    def evaluate(self, geCalc):
        print('Chosen tags:')
        pprint(self.tags)

        hits = 0
        tagCount = 0

        for tag in self.tags:
            tagCount += 1
            tagData = self.tags[tag]
            
            if evaluate_track_tag_predict(geCalc, self.precisionAt, tag, tagData['track']):
                print('Hit Tag: {}'.format(tagData['name']))
                hits += 1
            else:
                print('Missed Tag: {}'.format(tagData['name']))

        print('Hit Rate: {}'.format(hits / tagCount))


# ------------- static functions ------------

def evaluate_track_tag_predict(geCalc, precisionAt, tag, track):
    '''Evaluates tag prediction for tracks
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
