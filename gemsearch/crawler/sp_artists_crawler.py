
import spotipy
import spotipy.oauth2
from ratelimit import *
import json
import time
from pprint import pprint

from slack import slack_send_message, slack_error_message

@rate_limited(1)
def crawl_artist(sp, artistId):
    artist = sp.artist(artistId.strip())

    return artist

def create_artist_list(exportFileName):
    from gemsearch.storage.Storage import Storage
    artistCol = Storage().getCollection('artists')
    artists = artistCol.find({})

    with open(exportFileName, 'w', encoding="utf-8") as outFile:
        for artist in artists:
            outFile.write(str(artist['id']) + '\n')

def process_list(listPath, outputFileName):
    credentials = spotipy.oauth2.SpotifyClientCredentials('a82ae3d8bb5a4c4480189efa073efa94', '173c05b92b624c31ac97f6f961ac7462')
    token = credentials.get_access_token()
    sp = spotipy.Spotify(client_credentials_manager=credentials)
    
    missedFile = open('missed.csv', 'a')
    
    with open(outputFileName, 'a', encoding="utf-8") as resultFile:
        with open(listPath, 'r', encoding="utf-8") as idFile:
            for artistId in idFile:
                try:
                    result = crawl_artist(sp, artistId)
                except Exception as e:
                    # retry once
                    slack_error_message('Error (will retry): ', e)
                    time.sleep(120)
                    result = crawl_artist(sp, artistId)

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
    slack_send_message('Process list done')
