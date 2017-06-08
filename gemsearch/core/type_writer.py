from pprint import pprint
import csv

class TypeWriter:
    pathPrefix = ''

    def __init__(self, pathPrefix):
        self.pathPrefix = pathPrefix
        
        typeFile = open(pathPrefix + 'types.csv', 'w', encoding="utf-8")
        self.typeWriter = csv.writer(typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def addItem(self, data):
        print('AAAAADDD')
        self.typeWriter.writerow(data)
