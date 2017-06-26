from gemsearch.core.graph_generator import GraphGenerator
from gemsearch.core.id_manager import IdManager
from gemsearch.core.data_loader import traverseUserTrackInPlaylists, traverseTrackArtist, traverseTrackFeatures, traverseTrackTag

from gemsearch.evaluation.tag_prediction_evaluator import TagPredictionEvaluator
from gemsearch.embedding.node2vec import Node2vec
from gemsearch.embedding.ge_calc import GeCalc

dataDir = 'data/tmp_generator/'
outDir = 'data/run1/'


tagPredictEval = TagPredictionEvaluator(testSplit=0.2, precisionAt = 5)

print('------------- generate graph -------------')

graphGenerator = GraphGenerator(outDir+'graph.txt', IdManager(outDir+'types.csv'))

graphGenerator.add(traverseUserTrackInPlaylists(dataDir+'playlist.csv'))
graphGenerator.add(traverseTrackArtist(dataDir+'track_artist.csv'))
graphGenerator.add(traverseTrackFeatures(dataDir+'track_features.json'))
#graphGenerator.add(traverseTrackTag(dataDir+'track_tag.csv'))
graphGenerator.add(tagPredictEval.traverse(traverseTrackTag(dataDir+'track_tag.csv')))
graphGenerator.close_generation()


print('------------- graph embedding -------------')

em = Node2vec(50, 1, 80, 10, 10, 1, 1)
em.learn_embedding(outDir+'graph.txt', outDir+'node2vec.em')

geCalc = GeCalc()
geCalc.load_node2vec_data(outDir+'node2vec.em', outDir+'types.csv')


print('------------- evaluation -------------')


tagPredictEval.evaluate(geCalc)


print('------------- done -------------')
