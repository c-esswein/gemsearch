'''Generates unique mapping for uids to int indices.
'''
import csv
from gemsearch.core.data_loader import traverseTypes

class IdManager():

    def __init__(self, outputFile, typeHandlers = [], extendExistingFile = False):
        fileMode = 'w'
        if extendExistingFile:
            fileMode = 'a'

        self._typeFile = open(outputFile, fileMode, encoding="utf-8")
        self._typeWriter = csv.writer(self._typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self._typeHandlers = typeHandlers
        
        self._lookupDict = {}
        self._idCounter = 0

    def getId(self, item):
        ''' Returns numeric id for given item.
        '''
        uid = str(item['id'])

        if not uid in self._lookupDict:
            self._lookupDict[uid] = self._idCounter
            self.writeItem(self._idCounter, uid, item['type'], item['name'])
            self._idCounter += 1

        return str(self._lookupDict[uid])

    def writeItem(self, idCounter, uidObj, type, name):
        '''called when new id was generated for item.
        '''
        self._typeWriter.writerow([idCounter, uidObj, type, name])

        for typeHandler in self._typeHandlers:
            typeHandler.addItem(idCounter, uidObj, type, name)

    def close(self):
        self._typeFile.close()

        for typeHandler in self._typeHandlers:
            typeHandler.close_handler()

    def loadExisting(self, filePath):
        ''' Load existing lookup.
        '''
        for typeDef in traverseTypes(filePath):
            self._lookupDict[typeDef['id']] = typeDef['embeddingIndex']
            self._idCounter = typeDef['embeddingIndex']
        
        # increase id counter to make sure next id is valid
        self._idCounter += 1

class NewTypeCollector():
    ''' Collects new types.
    '''

    def __init__(self):
        self._newTypes = []

    def addItem(self, idCounter, uidObj, type, name):
        self._newTypes.append({
            'embeddingIndex': idCounter,
            'id': uidObj,
            'type': type,
            'name': name
        })

    def close_handler(self):
        pass

    def getAddedEmbeddingIds(self):
        return [typeDef['embeddingIndex'] for typeDef in self._newTypes]

    def getAddedTypes(self):
        return self._newTypes
