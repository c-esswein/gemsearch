''' Assign edge weights from embedding distances.
'''

from gemsearch.core.data_loader import traverseGraphFile


def assign_edge_weights(graphFile, outFilePath, geCalc):
    ''' Reads input graph and assigns edge weights from embedding. Result is written
    to outFilePath as edge list.
    '''
    with open(outFilePath, 'w') as outFile:
        for edge in traverseGraphFile(graphFile):
            weight = geCalc.get_distance(edge[0], edge[1])
            outFile.write('{} {} {}\n'.format(edge[0], edge[1], weight))


if __name__ == '__main__':
    from gemsearch.embedding.ge_calc import GeCalc

    tmpDir = 'data/graph_50_data/'
    # embed_hope(tmpDir+'graph.txt', tmpDir+'hope.em')

    geCalc = GeCalc()
    geCalc.load_node2vec_data(tmpDir+'node2vec.em', tmpDir+'types.csv')

    assign_edge_weights(tmpDir+'graph.txt', tmpDir+'graph_weighted.txt', geCalc)

