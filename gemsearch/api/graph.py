import networkx as nx

class Graph():
    
    def load_from_edge_list(self, file_name, node_handler = None):
        with open(file_name, 'r') as f:
            G = nx.Graph()
            for line in f:
                edge = line.strip().split()
                if len(edge) == 3:
                    w = float(edge[2])
                else:
                    w = 1.0
                
                if (node_handler is not None):
                    validNodes = node_handler(int(edge[0])) and node_handler(int(edge[1]))
                    if validNodes == False:
                        continue

                G.add_edge(int(edge[0]), int(edge[1]), weight=w)
        self._G = G

    def get_edges(self):
        '''Get edge list. Node IDs are embedding indices.
        '''
        return self._G.edges()

    def get_neighbors(self, nodeId):
        return [n in self._G[nodeId]]
