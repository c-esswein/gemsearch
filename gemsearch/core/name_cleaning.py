'''Contains helper to clean entity names.
'''
import re

MIN_TAG_COUNT = 5 # minimum last fm tag count for track
MIN_NAME_LENGTH = 3 # minimum alpha chars a name must contain

def clean_playlist_name(name):
    '''Simple playlist name cleaning.
    '''
    name = name.strip()

    # check if at least one alpha char exist
    if not re.search('[a-zA-Z]', name):
        return False

    if len(name) < MIN_NAME_LENGTH:
        return False

    return name

def clean_tag(tag):
    '''Simple tag cleaning. Removes tags with small counts and
    cleans tag name. Returns False for bad names, cleaned name otherwise.
    '''
    if tag['count'] < MIN_TAG_COUNT:
        return False

    return clean_tag_name(tag['name'])

def clean_tag_name(name):
    '''Simple tag cleaning. Cleans tag name. Returns False for bad names, cleaned name otherwise.
    '''

    # remove - and "
    name = re.sub(r'[\-\"]', '', name)
    name = name.strip()


    if len(name) < MIN_NAME_LENGTH and not re.search('[0-9][0-9]', name):
        return False

    name = name.lower()

    return name
