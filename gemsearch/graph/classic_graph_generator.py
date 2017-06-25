
from gemsearch.graph.graph_generator import GraphGenerator

class ClassicGraphGenerator(GraphGenerator):

    def generateGraphItem(self, item):

        if item['type'] == 'playlist-track':
            self.writeConnection(item['user'], item['track'])

        if item['type'] == 'track-features':
            for feature in item['features']:
                self.writeConnection(feature['id'], item['track'], feature['val'])

        if item['type'] == 'track-artist':
            self.writeConnection(item['track'], item['artist'])

        if item['type'] == 'track-tag':
            self.writeConnection(item['track'], item['tag'])
