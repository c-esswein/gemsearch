import csv
from pprint import pprint
from gemsearch.storage.Storage import Storage

from gemsearch.core.iterator.user_track_iterator import UserTrackIterator
from gemsearch.graph.classic_graph_generator import ClassicGraphGenerator
from gemsearch.core.type_writer import TypeWriter

def generate_graph(csvFilePath, dataDir):
    csvFile = open(csvFilePath, 'r', encoding="utf-8")
    itemReader = csv.DictReader(csvFile, delimiter=',', quotechar='|')

    iterator = UserTrackIterator()
    graphGenerator = ClassicGraphGenerator(dataDir + 'graph.txt')

    for item in iterator.iterate([TypeWriter(dataDir + 'types.csv')], itemReader):
        graphGenerator.generateItem(item)

    graphGenerator.close_generation()

    print('generated graph')

def read_def_file(filePath):
    csvFile = open(filePath, 'r', encoding="utf-8")
    typeReader = csv.DictReader(csvFile, delimiter=',', quotechar='|')

    '''
    trackRepo = Storage().getCollection('tracks')
    # check tracks against db
    checked = {}
    found = 0
    missed = 0
    for row in typeReader:
        if row['track'] not in checked:
            trackData = trackRepo.find_one({'uri': row['track']})
            if trackData is not None:
                # print('found: ' + row['track'])
                found += 1
            else:
                missed += 1
            checked[row['track']] = True
            
    
    print('found: ' + str(found))
    print('missed: ' + str(missed))
    '''

    playlistRepo = Storage().getCollection('playlists')
    users = {}
    userCount = 0
    found = 0
    missed = 0
    for row in typeReader:
        if row['user'] not in users:
            userData = playlistRepo.find_one({'username': row['user']})
            if userData is not None:
                found += 1
            else:
                missed += 1
            users[row['user']] = True
            userCount += 1

    print('total users: ' + str(userCount))
    print('found: ' + str(found))
    print('missed: ' + str(missed))

def is_track_for_user(geCalc, userId, trackId):
    result = geCalc.query_by_ids([item['user']], ['track'])

    # get index of track
    recIndex = next(i for i, x in enumerate(result) if x['id'] == trackId)
    
    return recIndex < (len(result) / 2)


if __name__ == '__main__':
    read_def_file('data/ir2017.csv')
    
if __name__ == '__main__DD':
    tmpDir = 'data/ir2017/'

    #read_def_file('data/ir2017.csv')
    #generate_graph('data/ir2017_small.csv', tmpDir)

    #from gemsearch.embedding.default_embedder import DefaultEmbedder
    #DefaultEmbedder().start_embedding(tmpDir+'graph.txt', tmpDir+'embedding.em')


    from gemsearch.embedding.ge_calc import GeCalc
    geCalc = GeCalc()
    geCalc.load_node2vec_data(tmpDir+'embedding.em', tmpDir+'types.csv')

    csvFile = open('data/ir2017_small.csv', 'r', encoding="utf-8")
    itemReader = csv.DictReader(csvFile, delimiter=',', quotechar='|')

    for item in itemReader:
        recommend = is_track_for_user(geCalc, item['user'], item['track'])
        pprint(recommend)
