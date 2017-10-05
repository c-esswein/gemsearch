'''Handles creation of graphs.
'''


class GraphGenerator():
    _edges = []

    def __init__(self, storagePath, idManager):
        self._storagePath = storagePath
        self._idManager = idManager

    def addEdge(self, id1, id2, weight = 1):
        self._edges.append((id1, id2, weight))
    
    def addNode(self, item):
        return self._idManager.getId(item)

    def add(self, traverser):
        for item1, item2, weight in traverser:
            self.addEdge(self.addNode(item1), self.addNode(item2), weight)

    def getEdges(self):
        return self._edges

    def close_generation(self, extendExistingFile = False):
        ''' Finalizes generation and writes edges into file.
        '''
        # ge algos require list do be sorted...
        #self._edges.sort(key=lambda tup: tup[0])

        fileMode = 'w'
        if extendExistingFile:
            fileMode = 'a'

        with open(self._storagePath, fileMode) as outFile:
            for edge in self._edges:
                outFile.write(edge[0]+' '+edge[1]+' '+str(edge[2])+'\n')

        self._idManager.close()
