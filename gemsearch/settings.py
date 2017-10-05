import os
from dotenv import load_dotenv

load_dotenv('.env')

'''Api token to post status update to slack channels.
'''
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')

'''Set to true on windows systems to run linux programs with bash
'''
USE_WINDOWS_BASH = (os.environ.get('USE_WINDOWS_BASH') == 'True')



'''Spotify api client id.
'''
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

'''Spotify api client secret.
'''
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

'''Last fm api key.
'''
LASTFM_API_KEY = os.environ.get('LASTFM_API_KEY')
