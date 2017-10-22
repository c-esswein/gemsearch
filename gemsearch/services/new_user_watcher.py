''' Service which watches for new users to embedd.

Extends existing model with new users + tracks.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.embedding.embed_new_users import embedNewUsers
import time


# ---- config ----
dataDir = 'data/tmp_extend/'
outDir = 'data/tmp/'

# ---- /config ----

logger.info('started new user watcher service with config: %s', {
    'dataDir': dataDir,
    'outDir': outDir,
})


while (True):
    try:
        if embedNewUsers() > 0:
            logger.info('new users embedded, restart API')
            # TODO: restart api...
            # import os
            # os.system("sudo /etc/init.d/gemsearch restart")
    except Exception as e:
        logger.error('Error: %s', e)

    time.sleep(30)

