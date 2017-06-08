
import os

from gemsearch.core.runner import run_pipeline
from gemsearch.core.item_iterator import ItemIterator
from gemsearch.core.type_writer import TypeWriter
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
from gemsearch.embedding.default_embedding import DefaultEmbedding
from gemsearch.evaluation.default_evaluator import DefaultEvaluator

dataDir = 'data/tmp_test/'

# create data dir
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

run_pipeline(
    dataDir,
    ItemIterator(10), # optional: limit types
    typeHandlers = [TypeWriter(dataDir)],
    graphGenerator = ClassicGraphGenerator(dataDir),
    embedding = DefaultEmbedding(),
    evaluations = [DefaultEvaluator()]
)

