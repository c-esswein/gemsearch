#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
from io import open
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import logging

import deepwalk.graph as graph
import deepwalk.walks as serialized_walks
from deepwalk.skipgram import Skipgram
from gensim.models import Word2Vec

from six import text_type as unicode
from six import iteritems
from six.moves import range

import psutil
from multiprocessing import cpu_count

p = psutil.Process(os.getpid())
try:
    p.set_cpu_affinity(list(range(cpu_count())))
except AttributeError:
    try:
        p.cpu_affinity(list(range(cpu_count())))
    except AttributeError:
        pass

logger = logging.getLogger(__name__)


defaultConfig = dict(
  debug=False, log='INFO',  
  format='edgelist',
  max_memory_data_size=1000000000, workers=1,
  number_walks=10, walk_length=5, window_size=5, representation_size=64, seed=0, 
  undirected=True, vertex_freq_degree=False
)

def _extendWithDefaultConfig(params):
  # create config args with params and defaultConfig
  args = Namespace()
  
  # copy params
  for key in params:
    setattr(args, key, params[key])

  # copy default config params
  for key in defaultConfig:
    if not hasattr(args, key):
      setattr(args, key, defaultConfig[key])

  return args

def startDeepwalk(params):
  '''Start deepwalk embedding with given params. Params are extended using defaultConfig.
  Word2Vec model is returned.
  '''
  args = _extendWithDefaultConfig(params)
  return _process(args)

def _process(args):
  logger.info('started deepwalk with config: %s', args)

  if args.format == "adjlist":
    G = graph.load_adjacencylist(args.input, undirected=args.undirected)
  elif args.format == "edgelist":
    G = graph.load_edgelist(args.input, undirected=args.undirected)
  elif args.format == "mat":
    G = graph.load_matfile(args.input, variable_name=args.matfile_variable_name, undirected=args.undirected)
  else:
    raise Exception("Unknown file format: '%s'.  Valid formats: 'adjlist', 'edgelist', 'mat'" % args.format)

  num_nodes = len(G.nodes())
  num_walks = num_nodes * args.number_walks

  logger.info("Number of nodes: {}".format(num_nodes))
  logger.info("Number of walks: {}".format(num_walks))

  data_size = num_walks * args.walk_length

  logger.info("Data size (walks*length): {}".format(data_size))

  if data_size < args.max_memory_data_size:
    logger.info("Start Walking...")
    walks = graph.build_deepwalk_corpus(G, num_paths=args.number_walks,
                                        path_length=args.walk_length, alpha=0, rand=random.Random(args.seed))
    logger.info("Start Training...")
    model = Word2Vec(walks, size=args.representation_size, window=args.window_size, min_count=0, workers=args.workers)
  else:
    logger.info("Data size {} is larger than limit (max-memory-data-size: {}).  Dumping walks to disk.".format(data_size, args.max_memory_data_size))
    logger.info("Start Walking...")

    walks_filebase = args.output + ".walks"
    walk_files = serialized_walks.write_walks_to_disk(G, walks_filebase, num_paths=args.number_walks,
                                         path_length=args.walk_length, alpha=0, rand=random.Random(args.seed),
                                         num_workers=args.workers)

    logger.info("Start Training...")    
    walks = serialized_walks.combine_files_iter(walk_files)    
    model = Word2Vec(walks, size=args.representation_size, window=args.window_size, min_count=0, workers=args.workers)

    logger.info('Delete serialized walks')
    for walkFile in walk_files:
      os.remove(walkFile)
      
    ''' 
    logger.info("Counting vertex frequency...")
    if not args.vertex_freq_degree:
      vertex_counts = serialized_walks.count_textfiles(walk_files, args.workers)
    else:
      # use degree distribution for frequency in tree
      vertex_counts = G.degree(nodes=G.iterkeys())

    logger.info("Training...")
    sentences = serialized_walks.combine_files_iter(walk_files)
    model = Skipgram(sentences=sentences, vocabulary_counts=vertex_counts,
                     size=args.representation_size, node_count=num_nodes,
                     window=args.window_size, min_count=0, workers=args.workers)
    '''
  model.wv.save_word2vec_format(args.output)

  return model

def extendModel(prevModelPath, newNodes, newEdges, params):
  ''' Continue learning with existing model. Graph given with args.input needs
  to contain the new nodes.
  '''

  args = _extendWithDefaultConfig(params)
  logger.info('started deepwalk extend with config: %s', args)  

  logger.info('Load previous model and graph')  
  # load model and graph
  model = Word2Vec.load(prevModelPath)
  G = graph.load_edgelist(args.input, undirected=args.undirected)

  # append new edges
  for x,y, w in newEdges:
      G[x].append(str(y))
      if args.undirected:
        G[y].append(str(x))
  G.make_consistent()

  logger.info('Create random walks')
  # create new walks
  # TODO: new node is allways at start -> problem?
  newWalks = []
  for cnt in range(args.number_walks):
    for node in newNodes:
      node = str(node)
      path = G.random_walk(path_length=args.walk_length, rand=random.Random(args.seed), alpha=0, start=node)
      # loaded word2vec model contains strings --> cast to string array
      # newWalks.append([str(node) for node in path])
      newWalks.append(path)
    
  logger.info('Start training')  
  model.build_vocab(newWalks, update=True)
  model.train(newWalks, total_examples=model.corpus_count, epochs=model.iter)

  logger.info('Save new embedding')    
  model.wv.save_word2vec_format(args.output)
  return model

def main():
  parser = ArgumentParser("deepwalk",
                          formatter_class=ArgumentDefaultsHelpFormatter,
                          conflict_handler='resolve')

  parser.add_argument("--debug", dest="debug", action='store_true', default=False,
                      help="drop a debugger if an exception is raised.")

  parser.add_argument('--format', default='adjlist',
                      help='File format of input file')

  parser.add_argument('--input', nargs='?', required=True,
                      help='Input graph file')

  parser.add_argument('--matfile-variable-name', default='network',
                      help='variable name of adjacency matrix inside a .mat file.')

  parser.add_argument('--max-memory-data-size', default=1000000000, type=int,
                      help='Size to start dumping walks to disk, instead of keeping them in memory.')

  parser.add_argument('--number-walks', default=10, type=int,
                      help='Number of random walks to start at each node')

  parser.add_argument('--output', required=True,
                      help='Output representation file')

  parser.add_argument('--representation-size', default=64, type=int,
                      help='Number of latent dimensions to learn for each node.')

  parser.add_argument('--seed', default=0, type=int,
                      help='Seed for random walk generator.')

  parser.add_argument('--undirected', default=True, type=bool,
                      help='Treat graph as undirected.')

  parser.add_argument('--vertex-freq-degree', default=False, action='store_true',
                      help='Use vertex degree to estimate the frequency of nodes '
                           'in the random walks. This option is faster than '
                           'calculating the vocabulary.')

  parser.add_argument('--walk-length', default=40, type=int,
                      help='Length of the random walk started at each node')

  parser.add_argument('--window-size', default=5, type=int,
                      help='Window size of skipgram model.')

  parser.add_argument('--workers', default=1, type=int,
                      help='Number of parallel processes.')
  
  args = parser.parse_args([
                "--input",
                "data/tmp/graph.txt",
                "--output",
                "data/tmp/deepwalk.em",
                "--format",
                "edgelist",
                "--walk-length",
                "5"
            ])
  logger.info(args)

  _process(args)

if __name__ == "__main__":
  sys.exit(main())
