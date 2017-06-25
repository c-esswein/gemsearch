
import os

from gemsearch.core.runner import run_pipeline
from gemsearch.core.iterator.playlist_iterator import PlaylistIterator
from gemsearch.core.type_writer import TypeWriter
from gemsearch.core.type_counter import TypeCounter
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
from gemsearch.embedding.default_embedder import DefaultEmbedder
from gemsearch.embedding.dummy_embedder import DummyEmbedder
from gemsearch.evaluation.default_evaluator import DefaultEvaluator
from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
from gemsearch.query.elastic_search_filler import EsTypeWriter

dataDir = 'data/tmp1/'
playlistLimit = 10

# create data dir
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

playlistQueryEvaluator = PlaylistQueryEvaluator(dataDir)

run_pipeline(
    dataDir,
    iterator = {
        'iterator': PlaylistIterator(playlistLimit),
        'typeHandlers': [
            playlistQueryEvaluator, 
            TypeWriter(dataDir + 'types.csv'), 
            TypeCounter(), 
            # EsTypeWriter()
        ],
        'generators': [ClassicGraphGenerator(dataDir + 'graph.txt')],
    },
    embeddings = [DefaultEmbedder()],
    evaluations = [DefaultEvaluator(), playlistQueryEvaluator]
)

# shutdown computer
# os.system('shutdown -s')