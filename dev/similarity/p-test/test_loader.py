#/usr/bin/env python3

from keras.utils import np_utils
from keras.datasets import cifar10, cifar100, mnist, fashion_mnist

import numpy as np
from random import random

class Loader():

    def __init__(self):

        return None

    def load_cifar10(self):        

        # The data, split between train and test sets:
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
        
        # Convert to greyscale, normalize
        rgb_convert = [0.2989,0.5870,0.1140]
        x_train = np.dot(x_train, rgb_convert)/255
        x_test  = np.dot(x_test , rgb_convert)/255

        # Convert class vectors to binary class matrices.
        y_train = np_utils.to_categorical(y_train, 20)
        y_test  = np_utils.to_categorical(y_test, 20)

        # Reduce sizes to 50k
        x_train = x_train[0:50000]
        x_test  = x_test[0:50000]
        y_train = y_train[0:50000]
        y_test  = y_test[0:50000]

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

    def load_cifar100(self):        

        # The data, split between train and test sets:
        (x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode="coarse")
        
        # Convert to greyscale, normalize
        rgb_convert = [0.2989,0.5870,0.1140]
        x_train = np.dot(x_train, rgb_convert)/255
        x_test  = np.dot(x_test , rgb_convert)/255

        # Convert class vectors to binary class matrices.
        y_train = np_utils.to_categorical(y_train, 20)
        y_test  = np_utils.to_categorical(y_test, 20)

        # Reduce sizes to 50k
        x_train = x_train[0:50000]
        x_test  = x_test[0:50000]
        y_train = y_train[0:50000]
        y_test  = y_test[0:50000]

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

    def load_mnist(self):        

        # The data, split between train and test sets:
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # Reshape to 32x32, and normalize
        x_train = np.pad(x_train, pad_width=((0,0),(2,2),(2,2)), 
                         mode='constant', constant_values=0)/255       

        x_test = np.pad(x_test, pad_width=((0,0),(2,2),(2,2)), 
                         mode='constant', constant_values=0)/255   

        ## Add channel at end 
        x_train = x_train.reshape(x_train.shape[0], 32, 32, 1)
        x_test  = x_test.reshape(x_test.shape[0], 32, 32, 1)

        # Convert class vectors to binary class matrices.
        y_train = np_utils.to_categorical(y_train, 20)
        y_test  = np_utils.to_categorical(y_test, 20)

        # Reduce sizes to 50k
        x_train = x_train[0:50000]
        x_test  = x_test[0:50000]
        y_train = y_train[0:50000]
        y_test  = y_test[0:50000]

        '''
        print('x_train shape:', x_train.shape)
        print('x_train shape:', x_test.shape)
        print('x_train shape:', y_train.shape)
        print('x_train shape:', y_test.shape)
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')
        '''

        return [x_train, x_test, y_train, y_test]

    def load_fmnist(self):        

        # The data, split between train and test sets:
        (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

        # Reshape to 32x32, and normalize
        x_train = np.pad(x_train, pad_width=((0,0),(2,2),(2,2)), 
                         mode='constant', constant_values=0)/255       

        x_test = np.pad(x_test, pad_width=((0,0),(2,2),(2,2)), 
                         mode='constant', constant_values=0)/255   

        ## Add channel at end 
        x_train = x_train.reshape(x_train.shape[0], 32, 32, 1)
        x_test  = x_test.reshape(x_test.shape[0], 32, 32, 1)

        # Convert class vectors to binary class matrices.
        y_train = np_utils.to_categorical(y_train, 20)
        y_test  = np_utils.to_categorical(y_test, 20)

        # Reduce sizes to 50k
        x_train = x_train[0:50000]
        x_test  = x_test[0:50000]
        y_train = y_train[0:50000]
        y_test  = y_test[0:50000]

        '''
        print('x_train shape:', x_train.shape)
        print('x_train shape:', x_test.shape)
        print('x_train shape:', y_train.shape)
        print('x_train shape:', y_test.shape)
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')
        '''

        return [x_train, x_test, y_train, y_test]

    # p = 1 --> max A
    # p = 0 --> max B
    def join(self, A, B, p):
        # Merged dataset
        data = []
        
        # For each x,y,train,test
        for ind, val in enumerate(A):
            dset = []
            # For each sample
            for ind2,val2 in enumerate(val):
                if random() < p:
                    dset.append(A[ind][ind2])
                else:
                    dset.append(B[ind][ind2])
            # Append set of samples
            data.append(np.asarray(dset))

        return data




