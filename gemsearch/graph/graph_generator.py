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

    def close_generation(self):
        # ge algos require list do be sorted...
        #self._edges.sort(key=lambda tup: tup[0])

        with open(self._storagePath, 'w') as outFile:
            for edge in self._edges:
                outFile.write(edge[0]+' '+edge[1]+' '+str(edge[2])+'\n')

        self._idManager.close()
