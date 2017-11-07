''' Uses MyMediaLite to test user-item recommender on baseline methods.
https://github.com/zenogantner/MyMediaLite

To run the tool Mono is required:
http://www.mono-project.com/download

'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
import csv
from gemsearch.utils.proc import execute_cmd

from gemsearch.settings import USE_WINDOWS_BASH
# PATH_MY_MEDIA_LITE = '../my_media_lite/bin/item_recommendation'
PATH_MY_MEDIA_LITE = '../my_media_lite_build/item_recommendation'


def writeUserRating(filePath, userTrack):
    ''' Creates file with user track pairs to use as input for my media lite.
    '''
    logger.info('write user ratings file: %s', filePath)
    with open(filePath, 'w') as outputFile:
        csvWriter = csv.writer(outputFile, delimiter=',', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerows(userTrack)

def writeUserRatingEdges(filePath, userTrack):
    ''' Creates file with user track pairs to use as input for my media lite.
    userTrack is a list of edge data.
    '''
    logger.info('write user ratings file: %s', filePath)    
    with open(filePath, 'w') as outputFile:
        csvWriter = csv.writer(outputFile, delimiter=',', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for (user, track, weight) in userTrack:
            csvWriter.writerow([user['id'], track['id'], weight])


def evalRandom(trainingFilePath, testFilePath = None, crossValidation = None):
    ''' Evaluate with random recommender.
    '''
    logger.info('started evalRandom')
    return executeMyMediaLite(trainingFilePath, 'Random', testFilePath, crossValidation)  

def evalMostPopular(trainingFilePath, testFilePath = None, crossValidation = None):
    ''' Evaluate with MostPopular recommender.
    '''
    logger.info('started evalMostPopular')    
    return executeMyMediaLite(trainingFilePath, 'MostPopular', testFilePath, crossValidation) 

def evalUserKNN(trainingFilePath, testFilePath = None, crossValidation = None):
    ''' Evaluate with UserKNN recommender.
    '''
    logger.info('started evalUserKNN')    
    return executeMyMediaLite(trainingFilePath, 'UserKNN', testFilePath, crossValidation) 

def executeMyMediaLite(trainingFilePath, recommenderMethod, testFilePath = None, crossValidation = None):
    args = [PATH_MY_MEDIA_LITE]
    args.append("--training-file=%s" % trainingFilePath)
    args.append("--recommender=%s" % recommenderMethod)
    args.append("--measures=\"prec@5\"")

    if testFilePath is None and crossValidation is None:
        raise Exception('Either testFilePath or number of folds for crossValidation must be set')

    if crossValidation is None:
        args.append("--test-file=%s" % testFilePath)
    else:
        # args.append("--cross-validation=%s" % crossValidation)
        args.append("--test-ratio=0,2")
    
    try:
        execute_cmd(args, useBash = USE_WINDOWS_BASH)
    except Exception as e:
        logger.error('Failed to execute MyMediaLite', exc_info=True)
        raise Exception('MyMediaLite error')


if __name__ == '__main__':
    tmpDir = 'data/rec/'
    evalRandom(tmpDir+'media_lite_training.csv', tmpDir+'media_lite_test.csv')
    # evalMostPopular(tmpDir+'media_lite_training.csv', tmpDir+'media_lite_test.csv')
    # evalUserKNN(tmpDir+'media_lite_training.csv', tmpDir+'media_lite_test.csv')
