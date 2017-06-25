
class GraphGenerator:
    edges = []
    _storagePath = ''
    _edgeFilter = None

    def __init__(self, storagePath, edgeFilter = None):
        self._storagePath = storagePath
        self._edgeFilter = edgeFilter

    def generateItem(self, item):
        # check if type should be moddeled
        if (self._edgeFilter is not None) and (item['type'] not in self._edgeFilter):
            return

        # check if item is training only
        if (not 'trainingOnly' in item) or (not item['trainingOnly']):
            self.generateGraphItem(item)

    def writeConnection(self, item1, item2, weight = 1):
        #print(item1, item2, weight)
        # only add if item1 and item2 index is given (training item overwise)
        if (item1 is not None) and (item2 is not None):
            self.edges.append((item1, item2, weight))

    def close_generation(self):
        # ge algos require list do be sorted...
        self.edges.sort(key=lambda tup: tup[0])

        with open(self._storagePath, 'w') as outFile:
            for edge in self.edges:
                outFile.write(edge[0]+' '+edge[1]+' '+str(edge[2])+'\n')
