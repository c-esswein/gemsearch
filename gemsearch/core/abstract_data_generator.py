''''Can be used to generate data files. Writes data to
type specific files with cached file handlers.
'''
import json
import csv
from gemsearch.core.data_loader import traverseTypes

class ADataGenerator(object):

    def __init__(self, dataDir):
        self._handlers = {} 
        # map to mark object ids written   
        self._idWritten = {}

        self._dataDir = dataDir

    def _getHandler(self, fileName):
        ''' Get filehandler for given fileName.
        '''
        if fileName not in self._handlers:
            self._handlers[fileName] = open(fileName, 'w', encoding="utf-8")

        return self._handlers[fileName]

    def closeHandlers(self):
        ''' Closes all open file handlers.
        '''
        for handler in self._handlers:
            self._handlers[handler].close()

    def write(self, connectionName, data):
        ''' Outputs given data into connectionName file in csv format.
        '''
        fileName = self._dataDir + connectionName + '.csv'
        outputFile = self._getHandler(fileName)
        csvWriter = csv.writer(outputFile, delimiter=',', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(data)

    def writeJson(self, connectionName, data):
        ''' Outputs given data into connectionName file in json format.
        '''
        fileName = self._dataDir + connectionName + '.json'
        outputFile = self._getHandler(fileName)
        outputFile.write(json.dumps(data) + '\n')

    def setIdWritten(self, id):
        ''' Sets given id as written.
        '''
        self._idWritten[id] = True        

    def checkAndSaveIfWritten(self, id):
        ''' Checks if id was allready written. Function will return
        true after first usage with id.
        '''
        if id in self._idWritten:
            return True
        else:
            self._idWritten[id] = True
            return False

    def checkIfWritten(self, id):
        ''' Checks if id was allready written. 
        '''
        if id in self._idWritten:
            return True
        else:
            return False

    def loadWrittenIdsFromTypeFile(self, filePath):
        ''' Loads type file ids to make sure no items are exported again
        for online learning.
        '''

        for typeDef in traverseTypes(filePath):
            self._idWritten[typeDef['id']] = True
