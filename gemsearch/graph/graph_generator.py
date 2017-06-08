
class GraphGenerator:
    edges = []
    pathPrefix = ''

    def __init__(self, pathPrefix):
        self.pathPrefix = pathPrefix

    def write_connection(self, item1, item2, weight = 1):
        #print(item1, item2, weight)
        self.edges.append((item1, item2, weight))

    def close_generation(self):
        # ge algos require list do be sorted...
        self.edges.sort(key=lambda tup: tup[0])

        with open(self.pathPrefix + 'graph.txt', 'w') as outFile:
            for edge in self.edges:
                outFile.write(edge[0]+' '+edge[1]+' '+str(edge[2])+'\n')
