import networkx as nx
from gemsearch.core.data_loader import traverseGraphFile


class Graph():
    
    def load_from_edge_list(self, file_name, node_handler = None):
        G = nx.Graph()
        for edge in traverseGraphFile(file_name):
            # skip edge if one of the node_handler returns false                
            if (node_handler is not None):
                validNodes = node_handler(edge[0]) and node_handler(edge[1])
                if validNodes == False:
                    continue

            G.add_edge(edge[0], edge[1], weight=edge[2])
        self._G = G

    def get_edges(self):
        '''Get edge list. Node IDs are embedding indices.
        '''
        return self._G.edges()

    def get_neighbors(self, nodeId, depth):
        '''Get neighbors of node.
        '''
        # TODO sort by weight, use depth
        return self._G[nodeId]
