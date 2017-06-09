
class TypeCounter:
    '''Counts number of entities for each type. And prints statistics.
    '''

    counter = {}

    def addItem(self, idCounter, uidObj, type, name, obj = {}):
        if not type in self.counter:
            self.counter[type] = 0
        
        self.counter[type] += 1

    def close_type_handler(self):
        print('Collected items by type:')
        for type in self.counter:
            print('{}: {}'.format(type, self.counter[type]))
