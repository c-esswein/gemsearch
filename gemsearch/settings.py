import os
from dotenv import load_dotenv

load_dotenv('.env')

SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
