''' Playlist evaluation runner: Extracts query from playlist name
and tries to predict playlist tracks.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
import gemsearch.core.data_loader as data_loader

from gemsearch.core.type_counter import TypeCounter
from gemsearch.query.elastic_search_filler import es_clear_indices, es_load_all_types

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
# from gemsearch.embedding.node2vec import Node2vec
from deepwalk.runner import startDeepwalk
# import deepwalk.node2vec
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from pprint import pprint

# ---- config ----
parser = ArgumentParser("playlist eval",
                          formatter_class=ArgumentDefaultsHelpFormatter,
                          conflict_handler='resolve')
parser.add_argument('--tags', default=True, type=bool, help='Wether to embed tags.')
parser.add_argument('--album', default=True, type=bool, help='Wether to embed albums.')
parser.add_argument('--genre', default=True, type=bool, help='Wether to embed artist genres.')
args = parser.parse_args()


dataDir = 'data/full_model/'
outDir = 'data/rec/'

SHOULD_GENERATE_GRAPH = False
SHOULD_INDEX_ES = False
SHOULD_EMBED = False

TEST_PLAYLIST_SPLIT=0.2
PRECISION_AT=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]
USE_USER_IN_QUERY = True
        
# ---- /config ----

logger.info('started playlist eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_GENERATE_GRAPH': SHOULD_GENERATE_GRAPH,
    'SHOULD_INDEX_ES': SHOULD_INDEX_ES,
    'TEST_PLAYLIST_SPLIT': TEST_PLAYLIST_SPLIT,
    'PRECISION_AT': PRECISION_AT,
    'USE_USER_IN_QUERY': USE_USER_IN_QUERY,
    'SHOULD_EMBED': SHOULD_EMBED,
    'ARGS': args
})
 
with Timer(logger=logger, message='playlist_eval runner') as t:

    playlistEval = PlaylistQueryEvaluator(testSplit=TEST_PLAYLIST_SPLIT, precisionAt=PRECISION_AT, useUserContext=USE_USER_IN_QUERY)
    
    if SHOULD_EMBED:
        if SHOULD_GENERATE_GRAPH:
            if USE_USER_IN_QUERY:
                trainingPlaylists = playlistEval.traverseAndSplitPlaylists(data_loader.traversePlaylists(dataDir+'playlist.csv'))
                playlistEval.writeTestLists(outDir+'test_playlists.json')
            else:
                playlistEval.addPlaylists(data_loader.traversePlaylists(dataDir+'playlist.csv'))

            print('------------- generate graph -------------')
            with Timer(logger=logger, message='graph generation') as t:

                idManager = IdManager(outDir+'types.csv', 
                        typeHandlers = [TypeCounter()]
                )
                graphGenerator = GraphGenerator(outDir+'graph.txt', idManager)

                # graphGenerator.add(data_loader.traverseTrackFeatures(dataDir+'track_features.json'))
                # add tracks without features
                for track, feature, weight in data_loader.traverseTrackFeatures(dataDir+'track_features.json'):
                    idManager.getId(track)

                graphGenerator.add(data_loader.traverseTrackArtist(dataDir+'track_artist.csv'))
                if args.tags:
                    graphGenerator.add(data_loader.traverseTrackTag(dataDir+'track_tag.csv'))
                if args.album:
                    graphGenerator.add(data_loader.traverseTrackAlbum(dataDir+'track_album.csv'))
                if args.genre:
                    graphGenerator.add(data_loader.traverseArtistGenre(dataDir+'artist_genre.csv'))

                if USE_USER_IN_QUERY:
                    graphGenerator.add(data_loader.traverseUserTrackInPlaylistsObj(trainingPlaylists))

                graphGenerator.close_generation()
        else:
            # reload existing split
            if USE_USER_IN_QUERY:
                playlistEval.loadTestLists(outDir+'test_playlists.json')
            else:
                playlistEval.addPlaylists(data_loader.traversePlaylists(dataDir+'playlist.csv'))

        if SHOULD_INDEX_ES:
            with Timer(logger=logger, message='elastic search writer') as t:
                # clear all current entries in elastic search
                es_clear_indices()

                # insert all types
                es_load_all_types(data_loader.traverseTypes(outDir+'types.csv'), 'music_index', 'music_type', dismissTypes = ['user'])

        
        # config for embedder factory
        config = dict(
            method='deepwalk',
            number_walks=20, walk_length=20, window_size=10, 
            representation_size=64, weighted = True
        )
        
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
                config['context_size'] = 10
                em = Node2vec(d=config['representation_size'], max_iter=1, ret_p=1, inout_p=1,
                    wLen=config['walk_length'], nWalks=config['number_walks'], cSize=config['context_size'])
                em.learn_embedding(config['input'], config['output'])
                # model = deepwalk.node2vec.embeddFromConfig(config)

            # model.save(outDir+'word2vecModel_'+name+'.p')
    
    else:
        playlistEval.loadTestLists(outDir+'test_playlists.json')

    # load embedding
    with Timer(logger=logger, message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'deepwalk.em', outDir+'types.csv')


    logger.info('------------- evaluation -------------')

    with Timer(logger=logger, message='evaluation') as t:
        res = playlistEval.evaluate(geCalc)

        # transform to array
        resList = [{'key': resKey, 'values': res[resKey]} for resKey in res]
        resList.sort(key=lambda runRes: runRes['values']['precision'])
        pprint(resList)


    print('------------- done -------------')