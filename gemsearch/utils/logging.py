import os
import json
import logging.config
import logging

# make sure setup is only executed once
_isInitialized = False

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    global _isInitialized

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    _isInitialized = True

def getLogger(name):
    ''' Returns new logger and initializes logging config
    if not set allready.
    '''
    global _isInitialized    
    if not _isInitialized:
        setup_logging()

    return logging.getLogger(name)    
