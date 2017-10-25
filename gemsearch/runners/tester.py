# Test user rec data set for validity
# TODO: delete

from pprint import pprint
import csv

outDir = 'data/full_model/'
trainingPath = outDir+'media_lite_training.csv'
testPath = outDir+'media_lite_test.csv'

def traverseUserTrack(filePath):
    with open(filePath, 'r', encoding="utf-8") as inFile:
        fieldnames = ['userId', 'trackId']
        for line in csv.DictReader(inFile, fieldnames=fieldnames, delimiter=',', quotechar='|'):            
            yield line

users = {}
tracks = {}

# traverse training and build track list and user track count
for line in traverseUserTrack(trainingPath):
    if not (line['userId'] in users):
        users[line['userId']] = 0
    
    users[line['userId']] += 1

    tracks[line['trackId']] = True

testUsers = {}
# traverse test
for line in traverseUserTrack(testPath):
    if not (line['userId'] in testUsers):
        testUsers[line['userId']] = 0
    
    # test count
    testUsers[line['userId']] += 1

    # check if user is in training
    if not (line['userId'] in users):
        print('user is missing in training: ' + str(line['userId']))    


for user in users:
    if users[user] < 10:
        print('user has not enough training samples:')
        pprint(users[user])
    if not user in testUsers:
        print('missing user in testUsers: ' + str(user))

for user in testUsers:
    if testUsers[user] < 8:
        print('len to small: ' + str(testUsers[user]) + ' ' + str(user))
    if not user in users:
        print('missing user in training: ' + str(user))

    if users[user] < testUsers[user]:
        print('more test thant training: ' + str(user))


print('usercount: ' +str(len(users)))
print('trackcount: ' +str(len(tracks)))

print('done')