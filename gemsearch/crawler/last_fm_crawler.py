'''Script to process list of missing tracks. Calls last fm api and stores
result into result file.
'''

from ratelimit import *
from urllib.parse import urlencode
import requests
from pprint import pprint
import csv
import json
import time

from gemsearch.utils.slack import slack_send_message, slack_error_message
from gemsearch.settings import LASTFM_API_KEY

from requests.adapters import HTTPAdapter

# retry every failed request 5 times
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))

@rate_limited(1)
def call_api(url):
    ''' get api response for given url
    '''
    response = s.get(url, timeout=15)

    if response.status_code != 200:
        if 'reason' in response:
            print(response['reason'])
        raise Exception('Cannot call API: {}'.format(response.status_code))

    return response


def getTagsForTrack(track):
    ''' Get tags for given track from last fm api.
        None is returned if track was not found.
    '''
    artistName = track['artists'][0]['name']
    trackName = track['name']
    return get_tags(artistName, trackName)

def get_tags(artistName, trackName):
    ''' Get tags for given track info from last fm api.
        None is returned if track was not found.
    '''
    if not artistName or not trackName:
        return None

    queryStr = urlencode({
         'method': 'track.gettoptags',
         'artist': artistName,
         'track': trackName,
         'api_key': LASTFM_API_KEY,
         'format': 'json'
    })
    url = 'http://ws.audioscrobbler.com/2.0/?' + queryStr
    
    response = call_api(url).json()
    if "error" in response:
        return None
    else:    
        return response['toptags']['tag']



# ---------------------------------
# ----------------- standalone list crawler methods
# ---------------------------------

def process_list(listPath, outputFileName):
    ''' process file with track info, result is written into single output file.
    '''
    csvFile = open(listPath, 'r', encoding="utf-8")
    typeReader = csv.reader(csvFile, delimiter=',', quotechar='|')

    resultFile = open(outputFileName, 'a')
    missedFile = open('missed.csv', 'a')

    try:
        for row in typeReader:
            trackId = row[0]
            artistName = row[1]
            trackName = row[2]

            try:
                tags = get_tags(artistName, trackName)
            except Exception as e:
                # retry once
                slack_error_message('Error (will retry): ', e)
                time.sleep(120)
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
                missedFile.write(trackId + '\n')
    finally:
        csvFile.close()
        resultFile.close()
        missedFile.close()

if __name__ == '__main__':
    try:
        process_list('last_fm_missing.csv', 'last_fm_result.json')
    except Exception as e:
        slack_error_message('Error: ', e)
        print(e)
    
    slack_send_message('Process list done')
