
import os

from gemsearch.core.runner import run_pipeline
from gemsearch.core.iterator.playlist_iterator import PlaylistIterator
from gemsearch.core.type_writer import TypeWriter
from gemsearch.core.type_counter import TypeCounter
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
# from gemsearch.query.elastic_search_filler import EsTypeWriter

# ---- config
dataDir = 'data/graph_100/'
playlistCount = 100
graphEdges = ['track-features', 'track-artist', 'track-tag']
# ---- config

# create data dir
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

run_pipeline(
    dataDir,
    iterator = {
        'iterator': PlaylistIterator(playlistCount),
        'typeHandlers': [
            TypeWriter(dataDir + 'types.csv'), 
            TypeCounter(), 
            # EsTypeWriter()
        ],
        'generators': [ClassicGraphGenerator(dataDir + 'graph.txt', graphEdges)],
    }
)
