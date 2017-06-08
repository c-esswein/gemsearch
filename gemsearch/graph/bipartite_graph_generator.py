
    def create_biparite_graph(self, outfile, limit):
        for item in self.get_items(limit):
            if item['type'] == 'user-playlist':
                self.write_connection(outfile, item['user'], item['playlist'])
            if item['type'] == 'track-artist':
                self.write_connection(outfile, item['user'], item['artist'])
            if item['type'] == 'playlist-track':
                self.write_connection(outfile, item['user'], item['track'])
            # tags missing