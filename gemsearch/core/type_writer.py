from pprint import pprint
import csv

class TypeWriter:
    
    def __init__(self, outputFile):        
        self.typeFile = open(outputFile, 'w', encoding="utf-8")
        self.typeWriter = csv.writer(self.typeFile, delimiter=',', lineterminator='\n',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

    def addItem(self, idCounter, uidObj, type, name, obj = {}):
        uri = ''
        if 'uri' in obj:
            uri = obj['uri']
            
        self.typeWriter.writerow([idCounter, uidObj, type, name, uri])

    def close_type_handler(self):
        self.typeFile.close()
