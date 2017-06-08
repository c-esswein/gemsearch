from pprint import pprint

''' is a evaluator and typeHandler
'''
class PlaylistQueryEvaluator:

    name = 'Playlist Query Evaluator'
    playlists = []

    def __init__(self, pathPrefix):
        self.pathPrefix = pathPrefix

    def addItem(self, idCounter, uidObj, type, name, obj = {}):
        if type == 'playlist':
            self.playlists.append(obj)

    def close_type_handler(self):
        print('playlist count: ' + str(len(self.playlists)))

    def evaluate(self, em):
        #TODO select n playlists..
        randomPlaylists = self.playlists

        for playlist in randomPlaylists:
            score = evaluate_playlist(playlist)
            print(score)

# ------------- static functions ------------

def evaluate_playlist(playlist):
    queryIds = extract_query_from_name(playlist['name'])
