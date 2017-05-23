from pprint import pprint
import numpy as np
import json
np.random.seed(1234)
#from sklearn.preprocessing import MinMaxScaler-
import keras.backend as K

dataInputFile = 'data/playlist-data-sample.json'

# returns feature vector for track
def getTrackFeatures(track):
    omitKeys = ['_id', 'track_id']
    data = []
    for key, value in track.items():
        if not key in omitKeys:
            data.append(value)
    return data

# creates test and training data
def getData(sequence_length=4, training_ratio=0.9):
    with open(dataInputFile, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    # map tracks to features array
    playlists = list(map(lambda playlist: 
            list(map(lambda track: getTrackFeatures(track), playlist['tracks'])), 
        data))

    playlists = np.array(playlists)
    np.random.shuffle(playlists)

    # pad tracks into equal sequences
    # TODO split and not truncate...
    playlists = pad_sequences(playlists, maxlen=sequence_length)

    row = round(training_ratio * playlists.shape[0])
    train = playlists[:row, :]
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = playlists[row:, :-1]
    y_test = playlists[row:, -1]

    # return playlists
    return [X_train, y_train, X_test, y_test]


def scalerTest():
    playlists = np.array([
        [[1,2,8],[2.1,3,8]],
        [[4,5,8],[6,7,8]],
        [[-2,0.2,8],[12,13.2,8]]
    ])

    #view = playlists[:,:,: 1]

    # flatten tracks
    s = playlists.shape
    trackView = playlists.reshape(s[0] * s[1], s[2])

    scaler = MinMaxScaler(feature_range=(0, 1), copy=False)
    scaler.fit_transform(trackView)

y_true = [[1,2,8], [1,2,9]]
y_pred = [[1,2,8], [1,2,9]]
val = K.mean(K.equal(y_true, y_pred), axis=-1)

pprint(val.tolist())