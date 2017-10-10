import logging
from io import open
from os import path
from time import time
from multiprocessing import cpu_count
import random
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

from six.moves import zip

from deepwalk import graph

logger = logging.getLogger("deepwalk")

__current_graph = None

# speed up the string encoding
__vertex2str = None

def count_words(file):
  """ Counts the word frequences in a list of sentences.

  Note:
    This is a helper function for parallel execution of `Vocabulary.from_text`
    method.
  """
  c = Counter()
  with open(file, 'r') as f:
    for l in f:
      words = l.strip().split()
      c.update(words)
  return c


def count_textfiles(files, workers=1):
  c = Counter()
  with ThreadPoolExecutor(max_workers=workers) as executor:
    for c_ in executor.map(count_words, files):
      c.update(c_)
  return c


def count_lines(f_path):
  ''' Counts number of lines in file. Returns 0 if file does not exist.
  '''
  if path.isfile(f_path):
    with open(f_path) as file:
      num_lines = sum(1 for line in file)
      return num_lines
  else:
    return 0

def _write_walks_to_disk(args):
  num_paths, path_length, alpha, rand, f = args
  G = __current_graph
  t_0 = time()
  with open(f, 'w') as fout:
    for walk in graph.build_deepwalk_corpus_iter(G=G, num_paths=num_paths, path_length=path_length,
                                                 alpha=alpha, rand=rand):
      fout.write(u"{}\n".format(u" ".join(__vertex2str[v] for v in walk)))
  logger.debug("Generated new file {}, it took {} seconds".format(f, time() - t_0))
  return f

def write_walks_to_disk(G, filebase, num_paths, path_length, alpha=0, rand=random.Random(0), num_workers=cpu_count(),
                        always_rebuild=True):
  global __current_graph
  global __vertex2str
  __current_graph = G
  __vertex2str = {v:str(v) for v in G.nodes()}
  files_list = ["{}.{}".format(filebase, str(x)) for x in range(num_paths)]
  expected_size = len(G)
  args_list = []
  files = []

  if num_paths <= num_workers:
    paths_per_worker = [1 for x in range(num_paths)]
  else:
    paths_per_worker = [len(list(filter(lambda z: z!= None, [y for y in x])))
                        for x in graph.grouper(int(num_paths / num_workers)+1, range(1, num_paths+1))]

  with ThreadPoolExecutor(max_workers=num_workers) as executor:
    line_counts = executor.map(count_lines, files_list)
    for size, file_, ppw in zip(line_counts, files_list, paths_per_worker):
      if always_rebuild or size != (ppw*expected_size):
        args_list.append((ppw, path_length, alpha, random.Random(rand.randint(0, 2**31)), file_))
      else:
        files.append(file_)

  with ThreadPoolExecutor(max_workers=num_workers) as executor:
    for file_ in executor.map(_write_walks_to_disk, args_list):
      files.append(file_)
  
  return files


def combine_files_iter(file_list):  
  # word2vec does not accept generators for sentences anymore:
  # TypeError, You can't pass a generator as the sentences argument. Try an iterator.
  # --> custom iterator which uses generator.
  return CombineFileIterator(file_list)

def combine_files_generator(file_list):
  for fPath in file_list:
    with open(fPath, 'r') as f:
      for line in f:
        yield line.split()

class CombineFileIterator(object):
  ''' Custom iterator which uses generator to traverse over all
  lines in provided files.
  '''
  def __init__(self, file_list):
      self.file_list = file_list

  def __iter__(self):
    self.generator = combine_files_generator(self.file_list)
    return self

  def __next__(self):
    return self.generator.__next__()
