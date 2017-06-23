"""Iterate base class.
"""


class ItemIterator:
    typeHandlers = []
    idCounter = 0
    lookupDict = {}
    limit = 0

    def __init__(self, limit = 10):
        self.limit = limit

    def getId(self, uidObj, type, name, obj = {}):
        '''Returns unique int identifier
        '''
        uid = str(uidObj)
        if not uid in self.lookupDict:
            self.lookupDict[uid] = self.idCounter
            self.newItemId(self.idCounter, uid, type, name, obj)
            self.idCounter += 1
        
        return str(self.lookupDict[uid])
    
    def newItemId(self, idCounter, uidObj, type, name, obj = {}):
        '''called when new item is iterated
        '''
        for typeHandler in self.typeHandlers:
            typeHandler.addItem(idCounter, uidObj, type, name, obj)

    def iterate(self, typeHandlers):
        ''' Generator with all items in db.
        '''
        self.typeHandlers = typeHandlers
