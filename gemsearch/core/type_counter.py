
from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)

class TypeCounter:
    '''Counts number of entities for each type and prints statistics.
    '''

    _counter = {}

    def addItem(self, idCounter, uidObj, type, name):
        if not type in self._counter:
            self._counter[type] = 0
        
        self._counter[type] += 1

    def close_handler(self):
        logger.info('Collected items by type:')
        totalCount = 0
        for type in self._counter:
            totalCount += self._counter[type]
            logger.info('{}: {}'.format(type, self._counter[type]))

        logger.info('-- Total: {} --'.format(totalCount))
