#/usr/bin/env python3
from PIL import Image

from keras.utils import np_utils
from keras.datasets import cifar100

from os import listdir
from os.path import isfile, join

import numpy as np
from sklearn.preprocessing import normalize

import random

from copy import deepcopy

class Loader():

    def __init__(self):
        return None

    def load_cifar100(self, classes=10):        

        # The data, split between train and test sets:
        (x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode="fine")
        
        # Convert to greyscale, normalize
        rgb_convert = [0.2989,0.5870,0.1140]
        x_train = np.dot(x_train, rgb_convert)/255
        x_test  = np.dot(x_test , rgb_convert)/255

        # Filter out classes above classes parameter
        # - train
        x_tmp = []
        y_tmp = []
        for ind,val in enumerate(y_train):
            if val[0] < classes:
                y_tmp.append(y_train[ind])
                x_tmp.append(x_train[ind])
        y_train = np.asarray(y_tmp)
        x_train = np.asarray(x_tmp)
        # - test
        x_tmp = []
        y_tmp = []
        for ind,val in enumerate(y_test):
            if val[0] < classes:
                y_tmp.append(y_test[ind])
                x_tmp.append(x_test[ind])
        y_test = np.asarray(y_tmp)
        x_test = np.asarray(x_tmp)

        # Convert class vectors to binary class matrices.
        y_train = np_utils.to_categorical(y_train, classes)
        y_test  = np_utils.to_categorical(y_test, classes)

        # Reduce sizes to 50k
        #x_train = x_train[0:50000]
        #x_test  = x_test[0:50000]
        #y_train = y_train[0:50000]
        #y_test  = y_test[0:50000]

        ## Add channel at end
        x_train = x_train.reshape(x_train.shape[0], 32, 32, 1)
        x_test  = x_test.reshape(x_test.shape[0], 32, 32, 1)

        '''
        print('x_train shape:', x_train.shape)
        print('x_train shape:', x_test.shape)
        print('x_train shape:', y_train.shape)
        print('x_train shape:', y_test.shape)
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')
        '''

        return [x_train, x_test, y_train, y_test]

