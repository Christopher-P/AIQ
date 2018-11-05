'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

from keras.utils import np_utils

from keras.datasets import mnist

import csv

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train = x_train / 255
x_test = x_test / 255

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

def logit(data):
    with open('data_cifar.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(data)

def gen_model(x,y):

    model = Sequential()
    model.add(Conv2D(8,  kernel_size=(3,3), activation='relu', input_shape=x.shape))
    model.add(Conv2D(16, kernel_size=(3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.2))
    model.add(Conv2D(16, kernel_size=(3,3), activation='relu'))
    model.add(Conv2D(8,  kernel_size=(3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(y, activation='softmax'))
    return model

model = gen_model(x_train[0], num_classes)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
data = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=50, batch_size=200, verbose=2)

logit(data.history['val_acc'])

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


