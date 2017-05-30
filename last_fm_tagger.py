from ratelimit import *
from pprint import pprint
import requests
from urllib.parse import urlencode
from Tracks import Tracks
from bson import ObjectId
from skip_ids import SKIP_IDS

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


if __name__ == '__main__':
    
    trackRepo = Tracks()
    trackCol = trackRepo.getTracks()

    tracks = trackCol.find({ 'tags' : { '$exists': False } }).limit(3000)
    missed = []

    skip = SKIP_IDS

    for track in tracks:
        # skip blacklisted items
        if track['_id'] in skip:
            continue

        artistName = track['artists'][0]['name']
        tags = get_tags(artistName, track['name'])
        if tags is not None:
            pprint('Update ' + str(track['_id']))
            trackCol.update_one({'_id': track['_id']}, {'$set': {'tags': tags}})
        else:
            pprint('Track not found: ' + str(track['_id']))
            missed.append(track)
    # pprint(get_tags('The Jam', 'The Dreams of Children'))
    pprint(list(map(lambda item: item['_id'], missed)))
    
