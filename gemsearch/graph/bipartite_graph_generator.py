
from gemsearch.graph.graph_generator import GraphGenerator

class ClassicGraphGenerator(GraphGenerator):

    def generateGraphItem(self, item):
        for item in self.get_items(limit):
            if item['type'] == 'user-playlist':
                self.writeConnection(item['user'], item['playlist'])
            if item['type'] == 'track-artist':
                self.writeConnection(item['user'], item['artist'])
            if item['type'] == 'playlist-track':
                self.writeConnection(item['user'], item['track'])
            # tags missing