''' Calculate baseline recommendation performance with my_media_lite
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
import gemsearch.evaluation.my_media_lite_evaluator as my_media_lite_eval
import gemsearch.core.data_loader as data_loader

# ---- config ----
dataDir = 'data/graph_100/'
outDir = 'data/user_rec/'
# ---- /config ----

# userTracks = data_loader.traverseUserTrackInPlaylists(dataDir+'playlist.csv')

logger.info('start writing data file')
# my_media_lite_eval.writeUserRatingEdges(outDir+'media_lite_training.csv', userTracks)

try:
    my_media_lite_eval.evalRandom(outDir+'media_lite_training.csv', outDir+'media_lite_test.csv')
except Exception as e:
    pass
try:
    my_media_lite_eval.evalMostPopular(outDir+'media_lite_training.csv', outDir+'media_lite_test.csv')
except Exception as e:
    pass
try:
    my_media_lite_eval.evalUserKNN(outDir+'media_lite_training.csv', outDir+'media_lite_test.csv')
except Exception as e:
    pass

