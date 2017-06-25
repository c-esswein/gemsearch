"""Iterate base class.
"""


class ItemIterator:
    typeHandlers = []
    trainingOnly = {}
    idCounter = 0
    lookupDict = {}
    limit = 0

    def __init__(self, limit = 10):
        self.limit = limit

    def getId(self, uidObj, type, name, obj = {}):
        '''Returns unique int identifier. If one of typeHandlers return False for addItem,
        then item is trainingOnly
        '''
        uid = str(uidObj)

        if uid in self.trainingOnly:
            return None

        if not uid in self.lookupDict:
            if self.newItemId(self.idCounter, uid, type, name, obj):
                self.lookupDict[uid] = self.idCounter
                self.idCounter += 1
            else:
                self.trainingOnly[uid] = True
                return None
        
        return str(self.lookupDict[uid])
    
    def newItemId(self, idCounter, uidObj, type, name, obj = {}):
        '''called when new item is iterated
        returns False if item should not be embedded.
        '''
        for typeHandler in self.typeHandlers:
            if typeHandler.addItem(idCounter, uidObj, type, name, obj):
                return False
        
        return True

    def iterate(self, typeHandlers):
        ''' Generator with all items in db.
        '''
        self.typeHandlers = typeHandlers
