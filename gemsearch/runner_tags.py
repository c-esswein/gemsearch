
import os

from gemsearch.core.runner import run_pipeline
from gemsearch.core.iterator import ItemIterator
from gemsearch.core.type_writer import TypeWriter
from gemsearch.core.type_counter import TypeCounter
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
from gemsearch.embedding.default_embedder import DefaultEmbedder
from gemsearch.evaluation.default_evaluator import DefaultEvaluator
from gemsearch.evaluation.tag_prediction_evaluator import TagPredictionEvaluator
from gemsearch.query.elastic_search_filler import EsTypeWriter

dataDir = 'data/tmp_tags/'

# create data dir
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

tagEvaluator = TagPredictionEvaluator(precisionAt = 5, firstNTags = 5)

run_pipeline(
    dataDir,
    iterator = {
        'iterator': ItemIterator(10),
        'typeHandlers': [
            TypeWriter(dataDir), 
            TypeCounter(), 
            tagEvaluator, 
            # EsTypeWriter()
        ],
        'generators': [ClassicGraphGenerator(dataDir), tagEvaluator],
    },
    embeddings = [DefaultEmbedder()],
    evaluations = [DefaultEvaluator(), tagEvaluator]
)
