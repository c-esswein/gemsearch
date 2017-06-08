
class GraphGenerator:

    def __init__(self, pathPrefix):
        self.outFile = open(pathPrefix + 'graph.txt', 'w')

    def write_connection(self, item1, item2, weight = 1):
        #print(item1, item2, weight)
        self.outFile.write(item1+' '+item2+' '+str(weight)+'\n')

    def close_generation(self):
        self.outFile.close()
