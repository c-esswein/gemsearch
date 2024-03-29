'''Create list of tracks without tag data. Import results of @last_fm_script.py
'''

from ratelimit import *
from pprint import pprint
import requests
from urllib.parse import urlencode
from bson import ObjectId
import csv
import json

from gemsearch.storage.Tracks import Tracks
from gemsearch.utils.slack import slack_send_message, slack_error_message
from .skip_ids import SKIP_IDS

def generate_list(exportFileName, limit = 1000):
    ''' generates csv list with missing tracks
    '''
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    tracks = trackCol.find({ 
        'tags' : { '$exists': False }, 
        '_id': { '$nin': SKIP_IDS }  # exclude blacklisted
        }).limit(limit) # .skip(limit*3)

    with open(exportFileName, 'w', encoding="utf-8") as typeFile:
        typeWriter = csv.writer(typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for track in tracks:
            artistName = track['artists'][0]['name']
            typeWriter.writerow([track['_id'], artistName, track['name']])
    

def process_missed():
    from gemsearch.crawler.last_fm_crawler import get_tags

    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    tracks = trackCol.find({ 
        'tags' : { '$exists': False }, 
        '_id': { '$in': SKIP_IDS }
    })
    
    for track in tracks:
        trackId = track['_id']
        if len(track['artists']) > 1:
            artistName = track['artists'][0]['name']
            tags = get_tags(artistName, track['name'])

            if tags is not None:
                pprint('Update ' + str(trackId))
                trackCol.update_one(
                    {'_id': trackId}, 
                    {'$set': {'tags': tags}}
                )
            else:
                pprint('Track not found: ' + str(trackId))

        else:
            print('no second artist: ' + str(trackId))

def import_update_file(filePath):
    ''' Imports result file into db
    '''
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    with open(filePath, 'r') as f:
        for line in f:
            dict_obj = json.loads(line)
            trackCol.update_one(
                {'_id': ObjectId(dict_obj['trackId'])}, 
                {'$set': {'tags': dict_obj['tags']}}
            )
            print('Updated: ' + dict_obj['trackId'])

if __name__ == '__main__':
    
    #generate_list('data/last_fm_missing-3.csv', 100000)
    #import_update_file('data/import/last_fm_result.json')
    process_missed()

    print("done")
