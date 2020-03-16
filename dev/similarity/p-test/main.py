#/usr/bin/env python3

from test_loader import Loader
import csv 

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

def gen_model(data):
    input_shape = (32,32,1)
    num_classes = data[2][0].shape[0]
    print(num_classes)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape,
                     data_format='channels_last'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    return model

def run_it(A, B, C):
    # Experiment Vars
    epochs = 12
    batch_size = 32

    results = []
    for i in [A,B,C]:
        model = gen_model(i)
        model.fit(i[0], i[2],
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(i[1], i[3]))
        score = model.evaluate(i[1], i[3], verbose=0)
        results.append(score[1])
    
    return results

def log_it(results):
    with open('results-label-joined.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)

def main():
    tl = Loader()
    tl.c10  = tl.load_cifar10()
    tl.c100 = tl.load_cifar100()
    tl.m    = tl.load_mnist()
    tl.fm   = tl.load_fmnist()

    names = ['MNIST', 'FMNIST', 'C10', 'C100']
    dats = [tl.m, tl.fm, tl.c10, tl.c100]
    for ind, val in enumerate(dats):
        for ind2, val2 in enumerate(dats):
            for i in range(11):
                p = i / 10.0
                tl.C = tl.join(val,val2,p)
                results = run_it(val, val2, tl.C)
                log_it([names[ind], names[ind2]] + results)

    return None

if __name__ == '__main__':
    main()
