''' User recommender evaluation runner. Uses collaborative filtering
to implement simple user-track recommender.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
import gemsearch.core.data_loader as data_loader

from gemsearch.core.type_counter import TypeCounter

from gemsearch.evaluation.user_evaluator import UserEvaluator
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer
from deepwalk.runner import startDeepwalk

import gemsearch.evaluation.my_media_lite_evaluator as my_media_lite_eval

from pprint import pprint

# ---- config ----
dataDir = 'data/full_model/'
outDir = 'data/rec/'

SHOULD_CREATE_GRAPH = True
SHOULD_EVAL_BASELINE = False

TEST_SPLIT=0.2
PRECISION_AT=[1, 5]
MIN_TRACKS_PER_USER = 30
# ---- /config ----

logger.info('started user rec eval with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_CREATE_GRAPH': SHOULD_CREATE_GRAPH,
    'SHOULD_EVAL_BASELINE': SHOULD_EVAL_BASELINE,
    'TEST_SPLIT': TEST_SPLIT,
    'PRECISION_AT': PRECISION_AT,
    'MIN_TRACKS_PER_USER': MIN_TRACKS_PER_USER,
})

with Timer(logger=logger, message='user_rec_evals runner') as t:

    userEval = UserEvaluator(testSplit=TEST_SPLIT, precisionAt=PRECISION_AT, minTracksPerUser = MIN_TRACKS_PER_USER)

    if SHOULD_CREATE_GRAPH:
        logger.info('------------- split training data -------------')
        trainingUserTrack = userEval.addUserTracks(data_loader.traverseUserTrackInPlaylists(dataDir+'playlist.csv'))
        userEval.writeTestData(outDir+'user_eval.pk')

        logger.info('------------- generate graph -------------')
        with Timer(logger=logger, message='graph generation') as t:
            idManager = IdManager(outDir+'types.csv', 
                typeHandlers = [TypeCounter()]
            )
            graphGenerator = GraphGenerator(
                outDir+'graph.txt', idManager
            )

            # graphGenerator.add(data_loader.traverseTrackFeatures(dataDir+'track_features.json'))
            # add tracks without features
            for track, feature, weight in data_loader.traverseTrackFeatures(dataDir+'track_features.json'):
                idManager.getId(track)

            graphGenerator.add(data_loader.traverseTrackArtist(dataDir+'track_artist.csv'))
            graphGenerator.add(data_loader.traverseTrackTag(dataDir+'track_tag.csv'))
            graphGenerator.add(data_loader.traverseTrackAlbum(dataDir+'track_album.csv'))
            graphGenerator.add(data_loader.traverseArtistGenre(dataDir+'artist_genre.csv'))                
            graphGenerator.add(trainingUserTrack)
            graphGenerator.close_generation()


        if SHOULD_EVAL_BASELINE:        
            # write files for MyMediaLite
            my_media_lite_eval.writeUserRatingEdges(outDir+'media_lite_training.csv', trainingUserTrack)
            my_media_lite_eval.writeUserRating(outDir+'media_lite_test.csv', userEval.getTestPairs())

    else:
        # load stored test data if not in embedding mode
        logger.info('No embedding + splitting, loading previous split')
        userEval.loadTestData(outDir+'user_eval.pk')


    if SHOULD_EVAL_BASELINE:
        # calculate baseline performance with my media lite
        my_media_lite_eval.evalRandom(outDir+'media_lite_training.csv', outDir+'media_lite_test.csv')
        my_media_lite_eval.evalMostPopular(outDir+'media_lite_training.csv', outDir+'media_lite_test.csv')
        my_media_lite_eval.evalUserKNN(outDir+'media_lite_training.csv', outDir+'media_lite_test.csv')

    logger.info('------------- graph embedding -------------')

    # config for embedder factory
    configs = [
        dict(
            number_walks=20, walk_length=20, window_size=10, 
            representation_size=64
        ),
        dict(
            number_walks=20, walk_length=20, window_size=10, 
            representation_size=128
        )
    ]

    results = []
    
    for config in configs:
        name = str(config['number_walks']) +'_'+ str(config['walk_length']) +'_'+ str(config['window_size'])
        name += '_'+ str(config['representation_size'])

        with Timer(logger=logger, message='embedding '+name) as t:
            # shared config
            config['input'] = outDir+'graph.txt'
            config['output'] = outDir+'deepwalk.em'
            config['workers'] = 3
            config['seed'] = 42
            config['max_memory_data_size'] = 7000000 # TODO: adapt mem size

            model = startDeepwalk(config)
            # model.save(outDir+'word2vecModel_'+name+'.p')
        

        # load embedding
        with Timer(logger=logger, message='ge calc initializing') as t:
            geCalc = GeCalc()
            geCalc.load_node2vec_data(config['output'], outDir+'types.csv')


        logger.info('------------- evaluation -------------')

        with Timer(logger=logger, message='evaluation') as t:
            res = userEval.evaluate(geCalc)
            results.append(res)

    # print total result json
    pprint(results)

    logger.info('------------- done -------------')

    
