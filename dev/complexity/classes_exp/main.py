#/usr/bin/env python3

from test_loader import Loader
import csv 

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

import random
import numpy as np

import datetime
import sys

def gen_model(data,nodes,layers):
    input_shape = (32,32,1)
    num_classes = data[3][0].shape[0]

    model = Sequential()
    model.add(Dense(nodes, activation='relu',
              input_shape=input_shape))

    for i in range(layers - 1):
        model.add(Dense(nodes, activation='relu'))

    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count

def run_it(A, nodes, layers):

    # Experiment Vars
    epochs = 12
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

def log_it(results):
    with open('data/results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)

def main():
    tl      = Loader()
    name = 'CIFAR'

    # get j from parameters
    for j in range(10):

        # num of classes --> 10,20,30,...,100
        classes = (j % 10 + 1) * 10
        dats = tl.load_cifar100(classes)

        # get random network params
        nodes  = int(random.random() * 32) + 1
        layers = int(random.random() * 5) + 1

        # Run exp
        results, tp, ntp  = run_it(dats, nodes, layers)

        # Save exp
        log_it([name, classes] + [nodes, layers, tp, ntp] + results)

    return None

if __name__ == '__main__':
    main()

