#/usr/bin/env python3

from test_loader import Loader
import csv 
import time

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

import random
import numpy as np

import datetime
import sys


def gen_model(data, nodes, layers):
    input_shape = (32, 32, 1)
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
                  verbose=0,
                  validation_data=(i[1], i[3]))
        score = model.evaluate(i[1], i[3], verbose=0)
        results.append(score[1])
    
    return results, tp, ntp


def log_it(name, results):
    with open('data_2/' + str(name) + '.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)


def main(start):
    # Number of samples (all domains)
    samples = 10

    # Get time for seed and file_name
    time = str(start)

    # Seed it
    random.seed(start)
    np.random.seed(int(start))

    ###Will run main code
    tl      = Loader()
    tl.cart   = tl.load_cartpole()
    tl.mnist = tl.load_mnist()
    tl.fmnist = tl.load_fmnist()
    tl.cifar10 = tl.load_cifar10()
    tl.cifar100 = tl.load_cifar100()

    print(len(tl.cart[0]))
    exit()

    names = ['MNIST', 'FMNIST', 'C10', 'C100', 'CARTPOLE']
    dats = [tl.mnist, tl.fmnist, tl.cifar10, tl.cifar100, tl.cart]

    for j in range(samples):
        for i in range(len(dats)):
            nodes = int(random.random() * 32) + 1
            layers = int(random.random() * 5) + 1
            results, tp, ntp = run_it(dats[i], nodes, layers)
            print(time, [names[i]] + [nodes, layers, tp, ntp] + results)
            log_it(time, [names[i]] + [nodes, layers, tp, ntp] + results)

    return None


if __name__ == '__main__':
    ## Parse args here
    start = time.time()
    main(start)
    done = time.time()
    elapsed = done - start
    print(elapsed)
