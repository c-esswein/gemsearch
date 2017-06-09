
import os

from gemsearch.core.runner import run_pipeline
from gemsearch.core.item_iterator import ItemIterator
from gemsearch.core.type_writer import TypeWriter
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
from gemsearch.embedding.default_embedder import DefaultEmbedder
from gemsearch.evaluation.default_evaluator import DefaultEvaluator
from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator

dataDir = 'data/tmp_test/'

# create data dir
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

# TODO:
    # - store playlists, query
    # - hide tags - evaluate

playlistQueryEvaluator = PlaylistQueryEvaluator(dataDir)

run_pipeline(
    dataDir,
    iterator = {
        'iterator': ItemIterator(10), # optional: limit types,
        'typeHandlers': [TypeWriter(dataDir), playlistQueryEvaluator],
        'generators': [ClassicGraphGenerator(dataDir)],
    },
    embeddings = [DefaultEmbedder()],
    evaluations = [DefaultEvaluator(), playlistQueryEvaluator]
)

