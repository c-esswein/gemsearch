
from gemsearch.graph.graph_generator import GraphGenerator

class ClassicGraphGenerator(GraphGenerator):

    def generateGraphItem(self, item):
        #print(item['type'])
        #if item['type'] == 'user-playlist':
        #    self.write_connection(item['user'], item['playlist'])
        if item['type'] == 'user-track':
            self.write_connection(item['user'], item['track'])
        if item['type'] == 'track-features':
            for feature in item['features']:
                self.write_connection(feature['id'], item['track'], feature['val'])
        if item['type'] == 'track-artist':
            self.write_connection(item['track'], item['artist'])
        if item['type'] == 'track-tag':
            self.write_connection(item['track'], item['tag'])
        if item['type'] == 'playlist-track':
            self.write_connection(item['playlist'], item['track'])
            self.write_connection(item['user'], item['track'])

