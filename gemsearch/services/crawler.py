''' Service which watches for new tracks.
Crawls track and artist metadata.

Checks for tracks without `gemsearch_status attribute`. After crawling `gemsearch_status=CRAWLED` is set.
'''
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

from gemsearch.crawler.combined_crawler import crawlNewTracks
import time

logger.info('started new crawler service: watching for new tracks')

while (True):
    try:
        crawlNewTracks()
    except Exception as e:
        logger.error('Error: %s', e)

    time.sleep(30)

