
    # TODO move into other cmp
    def get_graph_data(self):
        '''Get 3D graph coordinates for all items.
        '''
        # todo real 3d vecs
        return self.embedding[:,0:3].flatten()

    # TODO still needed?
    def get_lbl_mapping(self):
        '''Returns mapping from lables to items.
        '''
        return list(map(lambda lbl: self.get_item_info(lbl), self.embeddingLbl))

    # TODO move into other cmp
    def get_graph(self):
        '''Get edge list. Node IDs are embedding indices.
        '''
        nodes = read_graph_file(self.prefix + 'graph.txt')

        # transform lables into indices of embedding
        def get_i(lbl):
            return self.embeddingLbl.index(lbl)
        arr = list(map(lambda lbls: [get_i(lbls[0]), get_i(lbls[1])], nodes))
        return np.array(arr).flatten()

    def clean_graph(self):
        '''Removes all unused entries in graph. Only usefull if not fully connected
        graph is used.
        '''
        graph = self.get_graph()
        pprint(len(graph))

        with open(self.prefix + 'graph-cleaned.txt', 'w') as outfile:
            for pair in graph:
                if pair[0] in self.embeddingLbl and pair[1] in self.embeddingLbl:
                    outfile.write(str(pair[0])+' '+str(pair[1]) + '\n')

        return "removed unused entries"



def read_graph_file(file_name):
    '''Load Graph.
    '''
    connections = []
    with open(file_name, 'r') as f:
        for line in f:
            edge = line.strip().split()
            pointV = []
            for v in edge:
                pointV.append(int(v))
            connections.append(pointV)
    return connections

