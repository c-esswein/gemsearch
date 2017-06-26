'''Generates unique mapping for uids to int indices.
'''
import csv

class IdManager():
    _edges = []
    _lookupDict = {}
    _idCounter = 0
    _typeCounter = {}

    def __init__(self, outputFile):
        self._typeFile = open(outputFile, 'w', encoding="utf-8")
        self._typeWriter = csv.writer(self._typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def getId(self, item):
        uid = str(item['id'])

        if not uid in self._lookupDict:
            self._lookupDict[uid] = self._idCounter
            if 'name' not in item:
                item['name'] = ''
            self.writeItem(self._idCounter, uid, item['type'], item['name'])
            self._idCounter += 1

        return str(self._lookupDict[uid])

    def writeItem(self, idCounter, uidObj, type, name):
        self._typeWriter.writerow([idCounter, uidObj, type, name])

        if not type in self._typeCounter:
            self._typeCounter[type] = 0
        
        self._typeCounter[type] += 1

    def close(self):
        self._typeFile.close()

        print('Collected items by type:')
        for type in self._typeCounter:
            print('{}: {}'.format(type, self._typeCounter[type]))
