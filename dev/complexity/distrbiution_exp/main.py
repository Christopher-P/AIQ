import random
random.seed(123)
import numpy as np
np.random.seed(123)

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Input, Activation
from keras.optimizers import Adam
from keras.utils import to_categorical

import keras
from keras import backend as K

import csv

def log_it(results):
    with open('data/results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)


def gen_model(data,nodes,layers):

    model = Sequential()
    model.add(Flatten(input_shape=(1,10)))

    for i in range(layers - 1):
        model.add(Dense(nodes))
        model.add(Activation('relu'))

    model.add(Dense(2))
    model.add(Activation('linear'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count


def gen_data():
    n_samples = 50000
    n_bins = 2
    n_features = 10

    centers = [list(np.random.uniform(size=n_features)), list(np.random.uniform(size=n_features))]
    X, y = make_blobs(n_samples=n_samples, centers=centers, n_features=n_features, shuffle=True)

    # split train, test for calibration
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y,  test_size=0.9)

    # Correct the shape
    X_train = np.reshape(X_train, (len(X_train), 1, n_features))
    X_test = np.reshape(X_test, (len(X_test), 1, n_features))

    # Conv to one-hot
    y_train = to_categorical(y_train, n_bins)
    y_test = to_categorical(y_test, n_bins)

    return X_train, X_test, y_train, y_test, centers


def run_it(A, nodes, layers):

    # Experiment Vars
    epochs = 36
    batch_size = 32

    results = []
    for i in [A]:
        model, tp, ntp = gen_model(i, nodes, layers)
        model.fit(i[0], i[2],
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(i[1], i[3]))
        score = model.evaluate(i[1], i[3], verbose=0)
        results.append(score[1])
    
    return results, tp, ntp

def main():
    for j in range(500):
        # Generate data / package it
        X_train, X_test, y_train, y_test, centers = gen_data()
        data = [ X_train, X_test, y_train, y_test]

        # Gen random network params
        nodes = int(random.random() * 32) + 1
        layers = int(random.random()*5) + 1

        results, tp, ntp  = run_it(data, nodes, layers)
        log_it([centers, nodes, layers, tp, ntp] + results)
        

if __name__=="__main__": 
    main()

