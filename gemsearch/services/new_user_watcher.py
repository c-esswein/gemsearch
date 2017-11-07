''' Service which watches for new users to embedd.

Extends existing model with new users + tracks.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.embedding.embed_new_users import embedNewUsers
import time
from gemsearch.settings import GEMSEARCH_API_KEY, GEMSEARCH_API_URL
import requests
from pprint import pprint
from gemsearch.utils.slack import slack_send_message, slack_error_message

# ---- config ----
dataDir = 'data/tmp_extend/'
outDir = 'data/api/'

# ---- /config ----

logger.info('started new user watcher service with config: %s', {
    'dataDir': dataDir, 
    'outDir': outDir,
})


while (True):
    try:
        embeddedUserCount = embedNewUsers(dataDir, outDir)
        if embeddedUserCount > 0:
            logger.info('new users embedded, restart API')
            r = requests.get(str(GEMSEARCH_API_URL) + '/reload_embedding?token=' + str(GEMSEARCH_API_KEY))
            result = r.json()
            pprint(result)
            slack_send_message('api new user embedder included {} new users'.format(embeddedUserCount))
    except Exception as e:
        logger.error('Error: %s', e)
        slack_error_message('api new user embedder crashed (will not continue): ', e)
        break # TODO: remove?

    time.sleep(30)

