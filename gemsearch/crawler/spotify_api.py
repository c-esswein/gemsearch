''' Spotify api wrapper.
'''

import spotipy
import spotipy.oauth2
from ratelimit import *
import json
import time
from pprint import pprint

from gemsearch.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

@rate_limited(1)
def crawlArtist(sp, artistId):
    ''' Get artists data from spotify api
    '''
    artist = sp.artist(artistId.strip())

    return artist

@rate_limited(1)
def crawlTrack(sp, trackId):
    ''' Get tracks data from spotify api
    '''
    track = sp.track(trackId.strip())

    return track

def getSpotipyInstance():
    ''' Returns spotipy instance with valid credentials for crawling
    '''
    credentials = spotipy.oauth2.SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    token = credentials.get_access_token()
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    return sp

