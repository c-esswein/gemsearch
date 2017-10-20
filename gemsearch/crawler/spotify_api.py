''' Spotify api wrapper.
'''

import spotipy
import spotipy.oauth2
from ratelimit import *
import json
import time
from pprint import pprint

from gemsearch.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def crawlArtist(sp, artistId):
    ''' Get artists data from spotify api
    '''
    crawlingLock()    
    artist = sp.artist(artistId.strip())

    return artist

def crawlTrack(sp, trackId):
    ''' Get tracks data from spotify api
    '''
    crawlingLock()
    track = sp.track(trackId.strip())

    return track

@rate_limited(1)
def crawlingLock():
    ''' Make sure spotify api is not called more than once within one second.
    '''
    return True

def getSpotipyInstance():
    ''' Returns spotipy instance with valid credentials for crawling
    '''
    credentials = spotipy.oauth2.SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    token = credentials.get_access_token()
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    return sp

