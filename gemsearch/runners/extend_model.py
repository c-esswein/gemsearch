''' Generates embedding for api.
'''

from gemsearch.utils.logging import setup_logging
setup_logging()
import logging
logger = logging.getLogger(__name__)

from gemsearch.utils.timer import Timer
from deepwalk.runner import extendModel


# ---- config ----
dataDir = 'data/graph_50/'
outDir = 'data/tmp/'

# ---- /config ----

logger.info('started extend model embedding with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
})

with Timer(logger=logger, message='extend model') as t:

    graphFile = tmpDir+'graph.txt'
    existingModel = tmpDir+'word2vecModel.p'
    outputFile = tmpDir+'deepwalk_extended.em'

    newNodes = ['18505']
    newEdges = [('0','18505')]

    newModel = extendModel(existingModel, newNodes, newEdges, dict(
        input=graphFile, output=outputFile,
        number_walks=10, walk_length=5,
    ))
    
    newModel.save(tmpDir+'word2vecModel_new.p')
        