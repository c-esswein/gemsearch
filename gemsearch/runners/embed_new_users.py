''' Generates embedding for api.
'''

from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.type_counter import TypeCounter
from gemsearch.core.data_generator import DataGenerator
from gemsearch.core.id_manager import IdManager, NewIdCollector
from gemsearch.core.data_loader import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseUserTrack

from gemsearch.utils.timer import Timer
from deepwalk.runner import extendModel
import os.path

# ---- config ----
dataDir = 'data/tmp_extend/'
outDir = 'data/tmp/'

# ---- /config ----

logger.info('started extend model embedding with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
})


# TODO:
# - cannot execute twice (graph is not updated)
# - check which users are not embedded

with Timer(logger=logger, message='extend model') as t:

    graphFile = outDir+'graph.txt' # existing
    typeFile = outDir+'types.csv' # existing
    existingModel = outDir+'word2vecModel.p'
    outputFile = outDir+'deepwalk_extended.em'

    # --------------- export new data ---------------
    generator = DataGenerator(dataDir)
    generator.loadWrittenIdsFromTypeFile(typeFile)
    generator.writeUsers(5)
    generator.closeHandlers()

    # --------------- create new graph ---------------    
    logger.info('Create new graph')
    
    # create IdManager with previous embedding indices (object ids need to have same embedding indices)
    newNodeCollector = NewIdCollector()
    idManager = IdManager(typeFile, # old file will be extended
        typeHandlers = [TypeCounter(), newNodeCollector],
        extendExistingFile = True
    )
    idManager.loadExisting(typeFile)

    # generate new graph
    graphGenerator = GraphGenerator(
        graphFile, idManager
    )
    if os.path.isfile(dataDir+'track_features.json'):
        graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
    if os.path.isfile(dataDir+'track_artist.json'):
        graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
    if os.path.isfile(dataDir+'track_tag.json'):
        graphGenerator.add(traverseTrackTag(dataDir+'track_tag.csv'))
    if os.path.isfile(dataDir+'user_tracks.json'):
        graphGenerator.add(traverseUserTrack(dataDir+'user_tracks.csv'))
    graphGenerator.close_generation(extendExistingFile = True)

    # --------------- Extend existing model ---------------    
    newNodes = newNodeCollector.getAddedIds()
    newEdges = graphGenerator.getEdges()
    

    logger.info('Extend existing model')
    newModel = extendModel(existingModel, newNodes, newEdges, dict(
        input=graphFile, output=outputFile,
        number_walks=10, walk_length=5,
    ))
    
    logger.info('Save new model')
    newModel.save(outDir+'word2vecModel_new.p')
    

    # TODO: load new tracks / tags into elastic search
