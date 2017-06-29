
class TypeCounter:
    '''Counts number of entities for each type and prints statistics.
    '''

    _counter = {}

    def addItem(self, idCounter, uidObj, type, name):
        if not type in self._counter:
            self._counter[type] = 0
        
        self._counter[type] += 1

    def close_handler(self):
        print('Collected items by type:')
        for type in self._counter:
            print('{}: {}'.format(type, self._counter[type]))
