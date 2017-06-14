'''Utility for exporting crawled data.
'''

from pprint import pprint
import json

from gemsearch.storage.Tracks import Tracks
from gemsearch.utils.JSONEncoder import JSONEncoder

def export_tags(filePath):
    trackCol = Tracks().getTracks()
    tracks = trackCol.find({ 
        'tags' : { '$exists': True }
    })

    with open(filePath, 'w') as f:
        for track in tracks:
            item = {
                'track_uri': track['uri'],
                'tags': track['tags']
            }
            f.write(json.dumps(item))
            f.write('\n')

if __name__ == '__main__':
    
    export_tags('data/export/track-tags.json')

    print("done")
