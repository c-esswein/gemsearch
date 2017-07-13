from pprint import pprint

from gemsearch.graph.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traverseUserTrackInPlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag

from gemsearch.core.type_counter import TypeCounter

from gemsearch.evaluation.tag_prediction_evaluator import TagPredictionEvaluator
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

# ---- config ----
dataDir = 'data/graph_100/'
outDir = 'data/run1/'

TEST_TAG_SPLIT = 0.02
MAX_TOP_N_ACCURACY = 5
EMBEDDING_VERBOSE = False
# ---- /config ----

print('config:')
pprint({
    'dataDir': dataDir,
    'outDir': outDir,
    'TEST_TAG_SPLIT': TEST_TAG_SPLIT,
    'MAX_TOP_N_ACCURACY': MAX_TOP_N_ACCURACY
})

with Timer(message='playlist_eval runner') as t:
    tagPredictEval = TagPredictionEvaluator(testSplit=TEST_TAG_SPLIT, maxTopNAccuracy=MAX_TOP_N_ACCURACY)

    print('------------- generate graph -------------')
    with Timer(message='graph generation') as t:

        graphGenerator = GraphGenerator(
            outDir+'graph.txt', 
            IdManager(outDir+'types.csv', 
                typeHandlers = [TypeCounter()]
            )
        )

        graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
        graphGenerator.add(traverseUserTrackInPlaylists(dataDir+'playlist.csv'))
        graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
        graphGenerator.add(tagPredictEval.traverse(traverseTrackTag(dataDir+'track_tag.csv')))
        graphGenerator.close_generation()


    print('------------- graph embedding -------------')
    
    with Timer(message='embedding') as t:
        em = Node2vec(50, 1, 80, 10, 10, 1, 1, verbose=EMBEDDING_VERBOSE)
        em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')
    

    # load embedding
    with Timer(message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


    print('------------- evaluation -------------')
    
    with Timer(message='evaluation') as t:
        tagPredictEval.evaluate(geCalc)

    print('------------- done -------------')