from gemsearch.core.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.traverser.playlist import traversePlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag

from gemsearch.core.type_counter import TypeCounter
from gemsearch.query.elastic_search_filler import EsTypeWriter

from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc

dataDir = 'data/tmp_generator/'
outDir = 'data/run1/'


playlistEval = PlaylistQueryEvaluator(testSplit=0.2, precisionAt = 5)
playlistEval.addPlaylists(traversePlaylists(dataDir+'playlist.csv'))

print('------------- generate graph -------------')

graphGenerator = GraphGenerator(outDir+'graph.txt', IdManager(outDir+'types.csv', typeHandlers = [TypeCounter()]))

graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
graphGenerator.add(traverseTrackTag(dataDir+'track_tag.csv'))
graphGenerator.close_generation()


print('------------- graph embedding -------------')

em = Node2vec(50, 1, 80, 10, 10, 1, 1)
em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')

geCalc = GeCalc()
geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


print('------------- evaluation -------------')


playlistEval.evaluate(geCalc)


print('------------- done -------------')
