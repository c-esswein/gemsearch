
from gemsearch.utils.proc import execute_cmd
import logging
logger = logging.getLogger(__name__)

from gemsearch.settings import USE_WINDOWS_BASH

class Node2vec:
    def __init__(self, d, max_iter, wLen, nWalks, cSize, ret_p, inout_p, verbose = True):
        self._d = d
        self._max_iter = max_iter
        self._walkLength = wLen
        self._numWalks = nWalks
        self._contextSize = cSize
        self._return_p = ret_p
        self._inout_p = inout_p
        self._verbose = verbose

        self._method_name = 'node2vec_rw'
        self._X = None

    def learn_embedding(self, graphFile, outputFile = 'tempGraph.emb'):
        args = ['./gem/c_exe/node2vec']
        args.append("-i:%s" % graphFile)
        args.append("-o:%s" % outputFile)
        args.append("-d:%d" % self._d)
        args.append("-l:%d" % self._walkLength)
        args.append("-r:%d" % self._numWalks)
        args.append("-k:%d" % self._contextSize)
        args.append("-e:%d" % self._max_iter)
        args.append("-p:%f" % self._return_p)
        args.append("-q:%f" % self._inout_p)
        if self._verbose:
            args.append("-v")
        args.append("-dr")
        args.append("-w")
        
        try:
            execute_cmd(args, useBash = USE_WINDOWS_BASH)
        except Exception as e:
            logger.error('Failed to execute node2vec', exc_info=True)
            raise Exception('node2vec error')

if __name__ == '__main__':
    dataDir = 'data/viz/'
    em = Node2vec(3, 1, 80, 10, 10, 1, 1)
    em.learn_embedding(dataDir+'graph.txt', dataDir+'node2vec.em')
    print('result written to ' + dataDir+'node2vec.em')
