### Noise added to classificaiton data with known disimilarity
### Will verify Similarity method with this first method

# System utils
import os 
import sys
import csv

# Goto AIQ
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import os
from keras.utils import np_utils

import copy
import random
import numpy as np

# Import similarity util
from sim_util import Similarity

## Experiment parameters
seed = 123
proportion = 0.5
trials = 10
# p = 0.0 --> all B, p = 1.0 --> all A
## End parameters

def logger(Aname, Bname, r, A, B, AB, S):
    with open('r-noise.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([Aname, Bname, r, A, B, AB, S])
    return None

def gen_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=(32,32,1)))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    return model

def regen(x_train, r):
        x_rand = copy.deepcopy(x_train)
        for ind,val in enumerate(x_rand):
            rans = random.sample(range(0, 1024), r)

            for j in range(r):
                x_rand[ind][int(rans[j]/32)][int(rans[j]%32)] = random.random()
        
        return x_rand

def join(a,b):
    data = copy.deepcopy(a)
    for i in range(len(a)):
        if random.random() < 0.5:
            data[i] = b[i]
    return data

def main():

    ### Load data       
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    # Normalize xs
    x_train = x_train / 255
    x_test = x_test / 255

    # Convert to greyscale
    rgb_convert = [0.2989,0.5870,0.1140]
    x_train = np.dot(x_train, rgb_convert)
    x_test  = np.dot(x_test , rgb_convert)

    x_train = x_train.reshape(50000, 32, 32, 1)

    y_train = np_utils.to_categorical(y_train)
    y_test =  np_utils.to_categorical(y_test)

    ## Run experiment
    for i in range(10):
        
        model = gen_model()

        scoreA = model.fit(x_train, y_train, batch_size=32, epochs=20, validation_split=0.1)
        scoreA = scoreA.history['val_acc'][-1]

        model = gen_model()

        x_rand = regen(x_train, i*10)

        scoreB = model.fit(x_rand, y_train, batch_size=32, epochs=20, validation_split=0.1)
        scoreB = scoreB.history['val_acc'][-1]

        model = gen_model()

        merged = join(x_train,x_rand)

        scoreAB = model.fit(merged, y_train, batch_size=32, epochs=20, validation_split=0.1)
        scoreAB = scoreAB.history['val_acc'][-1]

        try:
            S = (abs(scoreA - scoreAB) - abs(scoreB - scoreAB)) / abs(scoreA - scoreB)
        except Exception as e:
            S= -100


        # Run it
        #A,B,AB,S = sim_backend.run(seed=seed,trials=trials,p=proportion)

        # Log it
        testA_name = 'CIFAR10'
        testB_name = 'CIFAR10_r' + str(i*10)
        logger(testA_name, testB_name, i*10, scoreA, scoreB, scoreAB, S)

if __name__ == "__main__":
    main()
