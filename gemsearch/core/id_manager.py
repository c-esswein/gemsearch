'''Generates unique mapping for uids to int indices.
'''
import csv

class IdManager():
    _edges = []
    _lookupDict = {}
    _idCounter = 0

    def __init__(self, outputFile, typeHandlers = []):
        self._typeFile = open(outputFile, 'w', encoding="utf-8")
        self._typeWriter = csv.writer(self._typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self._typeHandlers = []

    def getId(self, item):
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
            typeHandler.close()
