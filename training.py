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
def getData(sequence_length, ratio):
    with open('keras-test/data/playlist-data.json', "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    tracks = []
    for playlist in data:
        for track in playlist['tracks']:
            tracks.append(getTrackFeatures(track))

    tracks = np.array(tracks)

    row = round(0.9 * tracks.shape[0])
    train = tracks[:row, :]
    np.random.shuffle(train)
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = tracks[row:, :-1]
    y_test = tracks[row:, -1]

    # return tracks
    return [X_train, y_train, X_test, y_test]

# creates keras model
def createKerasModel(sequence_length, inputShape):
    import keras
    import tensorflow as tf

    from keras.models import Sequential  
    from keras.layers.core import Dense, Activation, Dropout
    from keras.layers.recurrent import LSTM
    
    in_out_neurons = inputShape[0] 

    '''
    hidden_neurons = 300
    model = Sequential()
    model.add(LSTM(hidden_neurons, input_shape=inputShape, return_sequences=False))
    model.add(Dense(in_out_neurons))
    model.add(Activation("linear"))
    
    model.compile(loss="mean_squared_error",
        optimizer="rmsprop",
        metrics=['accuracy'])
        '''

    model = Sequential()
    layers = [in_out_neurons, 50, 100, in_out_neurons]
    model.add(LSTM(
            input_shape=(None, layers[0]),
            units=layers[1],
            return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(
            layers[2],
            return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=layers[3]))
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
        return np.reshape(train, (train.shape[0], train.shape[1], 1))

    X_train = reshape_dataset(X_train)
    X_test = reshape_dataset(X_test)

    if model is None:
        model = createKerasModel(sequence_length, X_train.shape[1:])

    global_start_time = time.time()

    try:
        model.fit(
            X_train, y_train,
            batch_size=512, epochs=epochs, validation_split=0.05)
        predicted = model.predict(X_test)
        predicted = np.reshape(predicted, (predicted.size,))
    except KeyboardInterrupt:
        print('Training duration (s) : ', time.time() - global_start_time)
        return model, y_test, 0

run_network()

