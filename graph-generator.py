"""
Generates graph training set from mongodb
"""
from pprint import pprint
from Playlists import Playlists
from Tracks import Tracks
from Storage import Storage
import csv


playlists = Storage().getCollection('tmp_playlists_cleaned').find({}).limit(200)
tracksRepo = Tracks()

with open('data/types-all.csv', 'w', encoding="utf-8") as typeFile:
    typeWriter = csv.writer(typeFile, delimiter=',', lineterminator='\n',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    idCounter = 0
    lookupDict = {}
    
    # get uid and write type info
    def getId(uidObj, type, name):
        global idCounter
        uid = str(uidObj)
        if not uid in lookupDict:
            lookupDict[uid] = idCounter
            typeWriter.writerow([idCounter, type, uid, name])
            idCounter += 1
        
        return str(lookupDict[uid])

    with open('data/graph_200p.txt', 'w') as outfile:
        for playlist in playlists:
            userId = getId(playlist['username'], 'user', playlist['username'])
            outfile.write(userId+' '+getId(playlist['_id'], 'playlist', playlist['name']) + '\n')
            for track in playlist['tracks']:
                trackData = tracksRepo.getTrackById(track['track_id'])
                
                artists = []
                for artist in trackData['artists']:
                    outfile.write(userId+' '+getId(artist['id'], 'artist', artist['name']) + '\n')
                    artists.append(artist['name'])
                
                artistName = ' ++ '.join(artists)
                outfile.write(userId+' '+getId(track['track_id'], 'track', trackData['name'] + ' by: ' + artistName) + '\n')