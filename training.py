from pprint import pprint
import json

from sklearn.preprocessing import MinMaxScaler

import keras
import tensorflow as tf
from keras.models import Sequential  
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.preprocessing.sequence import pad_sequences

from JSONEncoder import JSONEncoder
import numpy as np
np.random.seed(1234)

# ---- config -----
#dataInputFile = 'data/playlist-data.json'
dataInputFile = 'data/playlist-data-10000.json'
network_config = {
    'epochs': 100,
    'ratio': 0.75,
    'sequence_length': 4
}
# ---- / config -----

scaler = MinMaxScaler(feature_range=(0, 1), copy=False)

# returns feature vector for track
def extract_features(track):
    omitKeys = ['_id', 'track_id']
    data = []
    for key, value in track.items():
        if not key in omitKeys:
            data.append(value)
    return data

# normalizes features
def normalize_data(playlists):
    s = playlists.shape
    trackView = playlists.reshape(s[0] * s[1], s[2])

    scaler.fit_transform(trackView)

# creates test and training data
def get_data(sequence_length, training_ratio):
    with open(dataInputFile, "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    # map tracks to features array
    playlists = list(map(lambda playlist: 
            list(map(lambda track: extract_features(track), playlist['tracks'])), 
        data))

    playlists = np.array(playlists)
    np.random.shuffle(playlists)

    # pad tracks into equal sequences
    # TODO split and not truncate...
    # TODO check value type
    playlists = pad_sequences(playlists, maxlen=sequence_length, dtype='float32')

    normalize_data(playlists)
    
    row = round(training_ratio * playlists.shape[0])
    train = playlists[:row, :]
    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = playlists[row:, :-1]
    y_test = playlists[row:, -1]

    # return playlists
    return [X_train, y_train, X_test, y_test]

# creates keras model
def create_model(inputShape):    
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
    model.compile(loss="mse", optimizer="rmsprop", metrics=['mse', 'mae', 'cosine'])

    # model.summary()

    return model

def run_network(model=None, data=None, sequence_length=network_config['sequence_length']):
    import time

    epochs = network_config['epochs']
    ratio = network_config['ratio']
    
    if data is None:
        print('Loading data... ')
        X_train, y_train, X_test, y_test = get_data(sequence_length, ratio)
    else:
        X_train, y_train, X_test, y_test = data
    
    print('\nData Loaded. Compiling...\n')

    if model is None:
        model = create_model(X_train.shape)

    global_start_time = time.time()

    try:
        model.fit(
            X_train, y_train,
            batch_size=512, epochs=epochs, validation_split=0.05)
    except KeyboardInterrupt:
        print('keyboard interrupt')
    finally:
        print('Training duration (s) : ', time.time() - global_start_time)
    
    evaluate_model(model, X_test, y_test)

    # print predicted
    predicted = model.predict(X_test)
    print('\nPredicted result:')
    print(json.dumps(y_test[0].tolist()))
    print(json.dumps(predicted[0].tolist()))

    return model

# evaluates model
def evaluate_model(model, X_test, y_test):
    print('\nEvaluate Model')
    scores = model.evaluate(X_test, y_test, batch_size=32)
    scoresLbld = list(zip(model.metrics_names, scores))
    print('evaluate result: {}, {}'.format(*scoresLbld))


run_network()