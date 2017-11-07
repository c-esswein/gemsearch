''' Generates embedding for api.
'''

from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.type_counter import TypeCounter
from gemsearch.core.data_generator import DataGenerator
from gemsearch.core.id_manager import IdManager, NewTypeCollector
import gemsearch.core.data_loader as data_loader
from gemsearch.api.user import getNewUsersForEmbedding, setUsersState
from gemsearch.query.elastic_search_filler import es_load_all_types

from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.graph.weight_assigner import assign_edge_weights
from gemsearch.embedding import dim_reducer

from gemsearch.utils.timer import Timer
from deepwalk.runner import extendModel
import os.path


def embedNewUsers(dataDir, outDir):
    ''' Checks db for new users and starts model extension if some exist.
    Returns number of new users.
    '''

    graphFile = outDir+'graph.txt' # existing
    typeFile = outDir+'types.csv' # existing
    existingModel = outDir+'word2vecModel.p' # existing
    outputFile = outDir+'embedding.em' # existing

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
        # graphGenerator.add(data_loader.traverseTrackFeatures(dataDir+'track_features.json'))
        # add tracks without features
        for track, feature, weight in data_loader.traverseTrackFeatures(dataDir+'track_features.json'):
            idManager.getId(track)
    if os.path.isfile(dataDir+'track_artist.csv'):
        graphGenerator.add(data_loader.traverseTrackArtist(dataDir+'track_artist.csv'))
    if os.path.isfile(dataDir+'track_tag.csv'):
        graphGenerator.add(data_loader.traverseTrackTag(dataDir+'track_tag.csv'))
    if os.path.isfile(dataDir+'user_tracks.csv'):
        graphGenerator.add(data_loader.traverseUserTrack(dataDir+'user_tracks.csv'))
    graphGenerator.close_generation(extendExistingFile = True)

    # --------------- Extend existing model ---------------    
    newNodes = newTypeCollector.getAddedEmbeddingIds()
    newEdges = graphGenerator.getEdges()
    
    logger.info('Extend existing model')
    newModel = extendModel(existingModel, newNodes, newEdges, dict(
        input=graphFile, output=outputFile,
        number_walks=10, walk_length=5, representation_size=64 #TODO: share config with api_embed
    ))
    
    logger.info('Save new model')
    newModel.save(existingModel) # override existing

    
    # recreate 3D model and weighted graph
    with Timer(logger=logger, message='weight assigning for graph') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outputFile, typeFile)

        assign_edge_weights(graphFile, outDir+'graph_w.txt', geCalc)

    with Timer(logger=logger, message='pca dimension reduction') as t:
        embedding = geCalc.embedding
        reduced = dim_reducer.pca(embedding)
        np.save(outDir+'pca.em', reduced)

    # set user states
    setUsersState(newUsers, 'EMBEDDED')

    # --------------- Insert new types into elastic search ---------------    
    logger.info('Insert new types into es')    
    newTypes = newTypeCollector.getAddedTypes()
    es_load_all_types(newTypes, 'music_index', 'music_type', dismissTypes = ['user'])

    return len(newUsers)
