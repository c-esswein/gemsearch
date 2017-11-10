''' Calculate baseline recommendation performance with my_media_lite
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
import gemsearch.evaluation.my_media_lite_evaluator as my_media_lite_eval
import gemsearch.core.data_loader as data_loader

# ---- config ----
dataDir = 'data/full_model/'
outDir = 'data/full_model_rec/'
extractData = False
# ---- /config ----

if extractData:
    userTracks = data_loader.traverseUserTrackInPlaylists(dataDir+'playlist.csv')

    logger.info('start writing data file')
    my_media_lite_eval.writeUserRatingEdges(outDir+'media_lite_training.csv', userTracks)

my_media_lite_eval.evalRandom(outDir+'media_lite_training.csv', crossValidation=True)
my_media_lite_eval.evalMostPopular(outDir+'media_lite_training.csv', crossValidation=True)
my_media_lite_eval.evalUserKNN(outDir+'media_lite_training.csv', crossValidation=True)
