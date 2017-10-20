''' Playlist evaluation runner: Extracts query from playlist name
and tries to predict playlist tracks.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseTypes, traverseUserTrackInPlaylistsObj

from gemsearch.core.type_counter import TypeCounter
from gemsearch.query.elastic_search_filler import es_clear_indices, es_load_all_types

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
# from gemsearch.embedding.node2vec import Node2vec
from deepwalk.runner import startDeepwalk
import deepwalk.node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

from pprint import pprint

# ---- config ----
dataDir = 'data/graph_15000/'
outDir = 'data/rec/'

SHOULD_GENERATE_GRAPH = True
SHOULD_INDEX_ES = True

TEST_PLAYLIST_SPLIT=0.2
PRECISION_AT=[1, 5, 10]
USE_USER_IN_QUERY = True
# ---- /config ----

logger.info('started playlist eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_GENERATE_GRAPH': SHOULD_GENERATE_GRAPH,
    'SHOULD_INDEX_ES': SHOULD_INDEX_ES,
    'TEST_PLAYLIST_SPLIT': TEST_PLAYLIST_SPLIT,
    'PRECISION_AT': PRECISION_AT,
    'USE_USER_IN_QUERY': USE_USER_IN_QUERY
})

with Timer(logger=logger, message='playlist_eval runner') as t:

    playlistEval = PlaylistQueryEvaluator(testSplit=TEST_PLAYLIST_SPLIT, precisionAt=PRECISION_AT, useUserContext=USE_USER_IN_QUERY)
    
    if SHOULD_GENERATE_GRAPH:
        if USE_USER_IN_QUERY:
            trainingPlaylists = playlistEval.traverseAndSplitPlaylists(traversePlaylists(dataDir+'playlist.csv'))
            playlistEval.writeTestLists(outDir+'test_playlists.json')
        else:
            playlistEval.addPlaylists(traversePlaylists(dataDir+'playlist.csv'))

        print('------------- generate graph -------------')
        with Timer(logger=logger, message='graph generation') as t:

            idManager = IdManager(outDir+'types.csv', 
                    typeHandlers = [TypeCounter()]
            )
            graphGenerator = GraphGenerator(outDir+'graph.txt', idManager)

            # graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
            # add tracks without features
            for track, feature, weight in traverseTrackFeatures(dataDir+'track_features.json'):
                idManager.getId(track)

            graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
            graphGenerator.add(traverseTrackTag(dataDir+'track_tag.csv'))

            if USE_USER_IN_QUERY:
                graphGenerator.add(traverseUserTrackInPlaylistsObj(trainingPlaylists))

            graphGenerator.close_generation()
    else:
        # reload existing split
        if USE_USER_IN_QUERY:
            playlistEval.loadTestLists(outDir+'test_playlists.json')
        else:
            playlistEval.addPlaylists(traversePlaylists(dataDir+'playlist.csv'))

    if SHOULD_INDEX_ES:
        with Timer(logger=logger, message='elastic search writer') as t:
            # clear all current entries in elastic search
            es_clear_indices()

            # insert all types
            es_load_all_types(traverseTypes(outDir+'types.csv'), 'music_index', 'music_type', dismissTypes = ['user'])

    
    # config for embedder factory
    configs = [
        dict(
            method='node2vec',
            number_walks=5, walk_length=5, window_size=5, 
            representation_size=64, weighted = True
        ),
        dict(
            method='node2vec',
            number_walks=20, walk_length=20, window_size=5, 
            representation_size=64, weighted = True
        ),
        dict(
            method='node2vec',
            number_walks=20, walk_length=20, window_size=10, 
            representation_size=64, weighted = True
        ),
        dict(
            method='deepwalk',
            number_walks=20, walk_length=20, window_size=10, 
            representation_size=64, weighted = True
        )
    ]

    results = {}
    
    for config in configs:
        name = str(config['number_walks']) +'_'+ str(config['walk_length']) +'_'+ str(config['window_size'])
        name += '_'+ str(config['representation_size'])
        name += '_'+ str(config['method'])

        with Timer(logger=logger, message='embedding '+name) as t:
            # shared config
            config['input'] = outDir+'graph.txt'
            config['output'] = outDir+'deepwalk.em'
            config['workers'] = 3
            config['seed'] = 42
            config['max_memory_data_size'] = 7000000 # TODO: adapt mem size

            if config['method'] == 'deepwalk':
                model = startDeepwalk(config)
            else:
                model = deepwalk.node2vec.embeddFromConfig(config)
            # model.save(outDir+'word2vecModel_'+name+'.p')
        

        # load embedding
        with Timer(logger=logger, message='ge calc initializing') as t:
            geCalc = GeCalc()
            geCalc.load_node2vec_data(config['output'], outDir+'types.csv')


        logger.info('------------- evaluation -------------')

        with Timer(logger=logger, message='evaluation') as t:
            res = playlistEval.evaluate(geCalc)
            results[name] = res
            pprint(res)


    # print total result json
    print('------------- done -------------')
    pprint(results)
