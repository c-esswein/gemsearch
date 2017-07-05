''''Can be used to generate data files. Writes data to
type specific files with cached file handlers.
'''
import json
import csv

class ADataGenerator():

    _handlers = {}

    def __init__(self, dataDir):
        self._dataDir = dataDir

    def _getHandler(self, fileName):
        if fileName not in self._handlers:
            self._handlers[fileName] = open(fileName, 'w', encoding="utf-8")

        return self._handlers[fileName]

    def _closeHandlers(self):
        for handler in self._handlers:
            self._handlers[handler].close()

    def write(self, connectionName, data):
        fileName = self._dataDir + connectionName + '.csv'
        outputFile = self._getHandler(fileName)
        csvWriter = csv.writer(outputFile, delimiter=',', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(data)

    def writeJson(self, connectionName, data):
        fileName = self._dataDir + connectionName + '.json'
        outputFile = self._getHandler(fileName)
        outputFile.write(json.dumps(data) + '\n')
