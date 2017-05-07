from pprint import pprint
import json
from JSONEncoder import JSONEncoder
import numpy as np
np.random.seed(1234)

# returns feature vector for track
def getTrackFeatures(track):
    omitKeys = ['_id', 'track_id']
    data = []
    for key, value in track.items():
        if not key in omitKeys:
            data.append(value)
    return data

# creates test and training data
def getData(sequence_length=12, ratio=0.5):
    with open('keras-test/data/playlist-data.json', "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    # map tracks to features
    playlists = list(map(lambda playlist: 
            list(map(lambda track: getTrackFeatures(track), playlist['tracks'])), 
        data))

    playlists = np.array(playlists)
    np.random.shuffle(playlists)

    row = round(0.9 * playlists.shape[0])
    train = playlists[:row, :]
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = playlists[row:, :-1]
    y_test = playlists[row:, -1]

    # return playlists
    return [X_train, y_train, X_test, y_test]

# creates keras model
def createKerasModel(inputShape):
    import keras
    import tensorflow as tf

    from keras.models import Sequential  
    from keras.layers.core import Dense, Activation, Dropout
    from keras.layers.recurrent import LSTM
    
    data_dim = inputShape[2]
    timesteps = inputShape[1]

    model = Sequential()
    model.add(LSTM(
            input_shape=(timesteps, data_dim),
            units=50,
            return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(
            100,
            return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=data_dim))
    model.add(Activation("linear"))
    model.compile(loss="mse", optimizer="rmsprop")

    # model.summary()

    return model

def run_network(model=None, data=None, sequence_length=12):
    import time

    epochs = 1
    ratio = 0.5
    
    if data is None:
        print('Loading data... ')
        X_train, y_train, X_test, y_test = getData(sequence_length, ratio)
    else:
        X_train, y_train, X_test, y_test = data
    
    print('\nData Loaded. Compiling...\n')

    def reshape_dataset(train):
        return np.reshape(train, (train.shape[0], train.shape[1], 10))

    #X_train = reshape_dataset(X_train)
    #X_test = reshape_dataset(X_test)

    if model is None:
        model = createKerasModel(X_train.shape)

    global_start_time = time.time()

    try:
        model.fit(
            X_train, y_train,
            batch_size=512, epochs=epochs, validation_split=0.05)
        predicted = model.predict(X_test)
        predicted = np.reshape(predicted, (predicted.size,))
        pprint(predicted)
        pprint(y_test)
    except KeyboardInterrupt:
        print('Training duration (s) : ', time.time() - global_start_time)
        return model, y_test, 0

run_network()