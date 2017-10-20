from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
import subprocess
from elasticsearch import Elasticsearch
import os
from gemsearch.settings import ELASTIC_SEARCH_EXECUTABLE
import signal

_managerInstance = None

###################################
# DOES NOT WORK --> terminating is buggy...
# not in use currently, set host with .env
###################################

class ElasticSearchInstance():
    ''' Class to start new instances of elasticsearch. Can be used to run
    evaluations on different database instances. Also makes sure that instance for the client api
    is not cleared.
    '''

    ''' Process instance of elastic search.
    '''
    _esProc = None

    _port = 9400


    def createInstance(self, dataPath, port = 9400, tcpPort = 9500):
        ''' Starts new elastic search instance. dataPath must be absolut or relative to elasticsearch
        executable.
        '''
        logger.info('create new elastic search instance on port %s', port)
        self._port = port

        args = [
            ELASTIC_SEARCH_EXECUTABLE,
            '-E', 'http.port=' + str(port),
            '-E', 'transport.tcp.port=' + str(tcpPort),
            '-E', 'path.data=' + str(dataPath),
        ]
        self._esProc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # log contains line like this:
        # [2017-10-20T12:02:05,000][INFO ][o.e.n.Node               ] [tnU4oTl] started

        logger.info('waiting for started state')        
        validStart = False
        startError = False
        for stdout_line in iter(self._esProc.stdout.readline, ''):
            print(stdout_line, end='')
            if stdout_line.find('exception') > -1:
                startError = True
                # do not break to print errors
            if stdout_line.find('started') > -1:
                validStart = True
                break
        
        if validStart and not startError:
            logger.info('instance ready')
        else:
            self._esProc.kill()
            raise Exception('Es instance could not be started')


    def getConnection(self):
        ''' Returns es connection for started db instance.
        '''
        es = Elasticsearch(
            ['localhost:' + str(self._port)],
            http_auth=('elastic', 'changeme')
        )
        return es

    def terminateInstance(self):
        ''' Terminate running instance.
        '''
        logger.info('terminate elastic search instance')        
        if not self._esProc is None:
            self._esProc.stdout.close()

            self._esProc.send_signal(signal.SIGTERM)           
            self._esProc.wait(20)
            # self._esProc.terminate()

    
    def __del__(self):
        print('__del__ was called')
        self.terminateInstance()

def getElasticSearchConnection():
    ''' get connection to elastic search.
    '''
    global _managerInstance

    # return local test instance
    if not _managerInstance is None:
        print('get test instance connection')
        return _managerInstance.getConnection()
    
    print('get default instace')

    # return default connection
    dbHost = os.environ.get('GEMSEARCH_ELASTICSEARCH_HOST', 'localhost')
    es = Elasticsearch(
        [dbHost],
        http_auth=('elastic', 'changeme')
    )

    return es

def getEsManager():
    ''' Singleton getter.
    '''
    global _managerInstance

    if _managerInstance is None:
        _managerInstance = ElasticSearchInstance()
    
    return _managerInstance
