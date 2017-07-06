import time

'''Print execution time for blocks. Usage:
from gemsearch.utils.timer import Timer

with Timer(message='Processing') as t:
    import time
    time.sleep(4)
# Processing... done in 4.002s

'''
class Timer(object):
    def __init__(self, message=None):
        self.start = None
        self.secs = None
        self.secs_str = None

        self.message = message

    def __enter__(self):
        if self.message:
            #print(self.message + '... ', end='', flush=True)
            print('%%% ' + self.message + '... ')

        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.secs = round(time.time() - self.start, 3)
        self.secs_str = str(self.secs) + 's'

        if self.message:
            print('\n%%% ' + self.message + ' done in', self.secs_str)