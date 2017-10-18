''' Standalone spotify artist list crawler.
Use to export a list of all artists and then process this list on other server.
Result is stored in json file which can be imported later.
'''

import json
import time
from pprint import pprint

from gemsearch.utils.slack import slack_send_message, slack_error_message
from gemsearch.crawler.spotify_api import crawlArtist

def create_artist_list(exportFileName):
    ''' Export all artist ids from db.
    '''
    from gemsearch.storage.Storage import Storage
    artistCol = Storage().getCollection('artists')
    artists = artistCol.find({})

    with open(exportFileName, 'w', encoding="utf-8") as outFile:
        for artist in artists:
            outFile.write(str(artist['id']) + '\n')

def process_list(listPath, outputFileName):
    ''' Process list of artist ids. Result is stored in single output file.
    '''
    sp = getSpotipyInstance()
    
    missedFile = open('missed.csv', 'a')
    
    with open(outputFileName, 'a', encoding="utf-8") as resultFile:
        with open(listPath, 'r', encoding="utf-8") as idFile:
            for artistId in idFile:
                try:
                    result = crawlArtist(sp, artistId)
                except Exception as e:
                    # retry once
                    slack_error_message('Error (will retry): ', e)
                    time.sleep(120)
                    result = crawlArtist(sp, artistId)

                if result is not None:
                    resultFile.write(json.dumps(result) + '\n')
                    pprint('Artist crawled: ' + artistId)
                else:
                    pprint('Artist not found: ' + artistId)
                    missedFile.write(artistId + '\n')


if __name__ == '__main__':
    # create_artist_list('data/artists.csv')
    process_list('data/artists.csv', 'data/crawled_artists.json')
    print('done')
    slack_send_message('Spotify Artist Process list done')
