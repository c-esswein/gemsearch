''' Generates embedding for api.
'''

from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.type_counter import TypeCounter
from gemsearch.core.data_generator import DataGenerator
from gemsearch.core.id_manager import IdManager, NewTypeCollector
from gemsearch.core.data_loader import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseUserTrack
from gemsearch.api.user import getNewUsersForEmbedding, setUsersState

from gemsearch.utils.timer import Timer
from deepwalk.runner import extendModel
import os.path


def embedNewUsers(dataDir, outDir):
    ''' Checks db for new users and starts model extension if some exist.
    Returns number of new users.
    '''

    graphFile = outDir+'graph.txt' # existing
    typeFile = outDir+'types.csv' # existing
    existingModel = outDir+'word2vecModel.p'
    outputFile = outDir+'deepwalk_extended.em'

    # --------------- export new data (user + new music) ---------------
    logger.info('Collect new users')    
    newUsers = getNewUsersForEmbedding()
    if len(newUsers) < 1:
        return 0
    logger.info('Found %s new users', len(newUsers))    

    generator = DataGenerator(dataDir)
    generator.loadWrittenIdsFromTypeFile(typeFile)
    for user in newUsers:
        generator.writeUser(user)
    generator.closeHandlers()

    # --------------- create new graph ---------------    
    logger.info('Create new graph')
    
    # create IdManager with previous embedding indices (object ids need to have same embedding indices)
    newTypeCollector = NewTypeCollector()
    idManager = IdManager(typeFile, # old file will be extended
        typeHandlers = [TypeCounter(), newTypeCollector],
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
    newNodes = newTypeCollector.getAddedEmbeddingIds()
    newEdges = graphGenerator.getEdges()
    
    logger.info('Extend existing model')
    newModel = extendModel(existingModel, newNodes, newEdges, dict(
        input=graphFile, output=outputFile,
        number_walks=10, walk_length=5,
    ))
    
    logger.info('Save new model')
    newModel.save(outDir+'word2vecModel_new.p')

    # set user states
    setUsersState(newUsers, 'EMBEDDED')

    # --------------- Insert new types into elastic search ---------------    
    logger.info('Insert new types into es')    
    newTypes = newTypeCollector.getAddedTypes()
    es_load_all_types(newTypes, 'music_index', 'music_type', dismissTypes = ['user'])

    return len(newUsers)
