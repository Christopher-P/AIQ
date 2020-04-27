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

def gen_model(data,nodes,layers):
    input_shape = (32,32,1)
    num_classes = data[3][0].shape[0]

    model = Sequential()
    model.add(Conv2D(nodes, (3, 3), activation='relu',
              input_shape=input_shape,data_format='channels_last'))

    for i in range(layers - 1):
        model.add(Conv2D(nodes, (3, 3), activation='relu'))

    model.add(Flatten())

    model.add(Dense(nodes, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count

def run_it(A, B, C, nodes, layers):

    # Experiment Vars
    epochs = 12
    batch_size = 32

    results = []
    for i in [A,B,C]:
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
    with open('many_agents.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)

def main():

    ###Will run main code
    tl      = Loader()
    tl.m    = tl.load_mnist()
    tl.fm   = tl.load_fmnist()

    names = ['MNIST', 'FMNIST']
    dats = [tl.m, tl.fm]

    ### Running for just comparing to cartpole!
    for ind in range(100):
        
        nodes  = int(random.random() * 32) + 1
        layers = int(random.random() *  5) + 1

        # Data comes from np-plot.py
        for i in range(0,11):
            p = i / 10.0
            tl.C = tl.join(tl.m, tl.m, p)
            results, tp, ntp  = run_it(tl.m, tl.m, tl.C, nodes, layers)
            log_it(['MNIST','MNIST'] + [nodes, layers, tp, ntp, p] + results)

        # Data comes from np-plot.py
        for i in range(0,11):
            p = i / 10.0
            tl.C = tl.join(tl.m, tl.fm, p)
            results, tp, ntp  = run_it(tl.m, tl.fm, tl.C, nodes, layers)
            log_it(['MNIST','FMNIST'] + [nodes, layers, tp, ntp, p] + results)

    return None

if __name__ == '__main__':
    main()
