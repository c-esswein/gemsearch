
import os
import sys
import codecs

from gemsearch.core.runner import run_pipeline
from gemsearch.core.item_iterator import ItemIterator
from gemsearch.core.type_writer import TypeWriter
from gemsearch.core.type_counter import TypeCounter
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
from gemsearch.embedding.default_embedder import DefaultEmbedder
from gemsearch.evaluation.default_evaluator import DefaultEvaluator
from gemsearch.evaluation.playlist_query_evaluator import PlaylistQueryEvaluator
from gemsearch.query.elastic_search_filler import EsTypeWriter

dataDir = 'data/tmp_test_2/'

# use utf-8 for stdout (playlist names contain sometimes strange chars)
if sys.stdout.encoding != 'utf-8':
  sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
  sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# create data dir
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

playlistQueryEvaluator = PlaylistQueryEvaluator()

run_pipeline(
    dataDir,
    iterator = {
        'iterator': ItemIterator(10),
        'typeHandlers': [
            TypeWriter(dataDir), 
            TypeCounter(), 
            playlistQueryEvaluator, 
            # EsTypeWriter()
        ],
        'generators': [ClassicGraphGenerator(dataDir)],
    },
    embeddings = [DefaultEmbedder()],
    evaluations = [DefaultEvaluator(), playlistQueryEvaluator]
)
