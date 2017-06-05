import string
from Playlists import Playlists
from Storage import Storage
import re
from nltk.stem import *
from nltk.tokenize import word_tokenize
from pprint import pprint

stemmer = PorterStemmer()

def clean_playlist_name(name):
    """ cleans name of playlist """
    # remove all non alpha numberic chars
    name = re.sub(r'[^a-zA-Z0-9\' ]', '', name)
    
    words = word_tokenize(name)
    stemmedWords = [stemmer.stem(word) for word in words]

    return stemmedWords

def clean_tags(tags):
    """ cleans tag name """

    def clean_tag(tag):
        return re.sub(r'[^a-zA-Z0-9\' ]', '', tag).lower().strip()
    
    output = set() # use set to make sure tags are unique
    for tag in tags:
        output.add(clean_tag(tag['_id']))
    
    return output

def check_from_repo():
    playlistRepo = Playlists()
    playlists = playlistRepo.getCollection().find({}).limit(10)

    for playlist in playlists:
        cleanedName = clean_playlist_name(playlist['name'])
        print(playlist['name'], ' || ', cleanedName)

if __name__ == '__main__':
    # check_from_repo()

    storage = Storage()
    tagRepo = storage.getCollection('tmp_tags')
    tags = tagRepo.find({}).limit(100)

    tags = clean_tags(tags)
    pprint(tags)
