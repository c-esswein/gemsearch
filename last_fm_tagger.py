from ratelimit import *
from pprint import pprint
import requests
from urllib.parse import urlencode
from Tracks import Tracks
from bson import ObjectId
from skip_ids import SKIP_IDS
from JSONEncoder import JSONEncoder
import csv
import json
from slack import slack_send_message, slack_error_message


API_KEY = 'f40c6192f19aabed7b3a48910c61587f'

@rate_limited(0.8)
def call_api(url):
  response = requests.get(url)

  if response.status_code != 200:
    if 'reason' in response:
        print(response['reason'])
    raise Error('Cannot call API: {}'.format(response.status_code))

  return response


def get_tags(artistName, trackName):
    if not artistName or not trackName:
        return None

    queryStr = urlencode({
         'method': 'track.gettoptags',
         'artist': artistName,
         'track': trackName,
         'api_key': API_KEY,
         'format': 'json'
    })
    url = 'http://ws.audioscrobbler.com/2.0/?' + queryStr
    
    response = call_api(url).json()
    if "error" in response:
        return None
    else:    
        return response['toptags']['tag']

def storeResultInFile(result, filePath):
    with open(filePath, 'w') as outfile:
        for chunk in JSONEncoder().iterencode(result):
            outfile.write(chunk)

def load_track(trackId):
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    track = trackCol.find_one({ 
        '_id': ObjectId(trackId)
    })
    pprint(track)

    artistName = track['artists'][0]['name']
    tags = get_tags(artistName, track['name'])
    pprint(tags)

def start_with_db(limit):
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    tracks = trackCol.find({ 
        'tags' : { '$exists': False }, 
        '_id': { '$nin': SKIP_IDS } # exclude blacklisted
        }).limit(limit)
    missed = []

    for track in tracks:
        artistName = track['artists'][0]['name']
        tags = get_tags(artistName, track['name'])
        if tags is not None:
            pprint('Update ' + str(track['_id']))
            trackCol.update_one({'_id': track['_id']}, {'$set': {'tags': tags}})
        else:
            pprint('Track not found: ' + str(track['_id']))
            missed.append(track)
    
    missedTransformed = list(map(lambda item: item['_id'], missed))
    pprint(missedTransformed)
    
    storeResultInFile(missedTransformed, 'missed-ids.json')

def generate_list(exportFileName, limit = 1000):
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    tracks = trackCol.find({ 
        'tags' : { '$exists': False }, 
        '_id': { '$nin': SKIP_IDS }  # exclude blacklisted
        }).limit(limit)

    with open(exportFileName, 'w', encoding="utf-8") as typeFile:
        typeWriter = csv.writer(typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for track in tracks:
            artistName = track['artists'][0]['name']
            typeWriter.writerow([track['_id'], artistName, track['name']])
    

def process_list(listPath, outputFileName):
    missed = []
    ddd = asdf

    return
    with open(listPath, 'r', encoding="utf-8") as csvfile:
        typeReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        with open(outputFileName, 'a') as resultFile:
            for row in typeReader:
                trackId = row[0]
                artistName = row[1]
                trackName = row[2]

                tags = get_tags(artistName, trackName)
                if tags is not None:
                    pprint('Update ' + str(trackId))
                    result = {
                        'trackId': trackId,
                        'tags': tags
                    }
                    resultFile.write(json.dumps(result))
                    resultFile.write('\n')
                else:
                    pprint('Track not found: ' + trackId)
                    missed.append(trackId)
    
    pprint(missed)
    
    storeResultInFile(missedTransformed, 'missed-ids.json')

    slack_send_message('Process list done')

def import_update_file(filePath):
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    with open(filePath, 'r') as f:
        for line in f:
            dict_obj = json.loads(line)
            trackCol.update_one({
                '_id': dict_obj['trackId']}, 
                {'$set': {'tags': dict_obj['tags']}
            })
            print('Updated: ' + dict_obj['trackId'])

if __name__ == '__main__':
    
    #generate_list('data/last_fm_missing.csv', 100000)
    '''try:
        process_list('data/last_fm_missing.csv', 'last_fm_result.json')
    except Exception as e:
        slack_error_message('Error: ', e)
    '''
    import_update_file('last_fm_result.json')
    #load_track('5730d37ea90a9a398df910d8')

    print("done")
