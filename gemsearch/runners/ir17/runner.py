from gemsearch.core.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traverseUserTrack, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag, traverseTypes

from gemsearch.core.type_counter import TypeCounter

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.utils.timer import Timer

from pprint import pprint

# ---- config ----
dataDir = 'data/ir17_data/'
outDir = 'data/ir17_data/'

SHOULD_EMBED = True

TEST_SPLIT=0.2
# ---- /config ----

print('config:')
pprint({
    'dataDir': dataDir,
    'outDir': outDir,
    'SHOULD_EMBED': SHOULD_EMBED,
    'TEST_SPLIT': TEST_SPLIT,
})

with Timer(message='ir17 runner') as t:

    if SHOULD_EMBED:
        print('------------- generate graph -------------')
        with Timer(message='graph generation') as t:

            graphGenerator = GraphGenerator(
                outDir+'graph.txt', 
                IdManager(outDir+'types.csv', 
                    typeHandlers = [TypeCounter()]
                )
            )

            graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
            graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
            graphGenerator.add(traverseTrackTag(dataDir+'track_tag.csv'))
            graphGenerator.add(traverseUserTrack(dataDir+'user_track.csv'))
            graphGenerator.close_generation()

        print('------------- graph embedding -------------')

        with Timer(message='embedding') as t:
            em = Node2vec(50, 1, 80, 10, 10, 1, 1, verbose=False)
            em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')

    # load embedding
    with Timer(message='ge calc initializing') as t:
        geCalc = GeCalc()
        geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


    print('------------- evaluation -------------')

    #with Timer(message='evaluation') as t:
        


    print('------------- done -------------')
