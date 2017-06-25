"""Iterates over user - track play history
"""

from gemsearch.core.iterator.item_iterator import ItemIterator
from gemsearch.storage.Storage import Storage
from gemsearch.storage.Tracks import Tracks


# TODO: not used! delte?

class UserTrackIterator(ItemIterator):

    def iterate(self, typeHandlers, history):
        ''' Generator with all items in db.
        '''
        super(UserTrackIterator, self).iterate(typeHandlers)

        featureId = self.getId('feature--valence', 'feature', 'feature--valence')
            
        for historyItem in history:
            userId = self.getId(historyItem['user'], 'user', historyItem['user'], {})
            trackId = self.getId(historyItem['track'], 'track', historyItem['track'], {})
            
            yield {
                'type': 'user-track',
                'user': userId,
                'track': trackId
            }
