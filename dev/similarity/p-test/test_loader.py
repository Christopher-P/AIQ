#/usr/bin/env python3

from keras.utils import np_utils
from keras.datasets import cifar10, cifar100, mnist, fashion_mnist

import numpy as np
import random

from copy import deepcopy

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
        y_train = np_utils.to_categorical(y_train, 10)
        y_test  = np_utils.to_categorical(y_test, 10)

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
        (x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode="fine")
        
        # Convert to greyscale, normalize
        rgb_convert = [0.2989,0.5870,0.1140]
        x_train = np.dot(x_train, rgb_convert)/255
        x_test  = np.dot(x_test , rgb_convert)/255

        # Convert class vectors to binary class matrices.
        y_train = np_utils.to_categorical(y_train, 100)
        y_test  = np_utils.to_categorical(y_test, 100)

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
        y_train = np_utils.to_categorical(y_train, 10)
        y_test  = np_utils.to_categorical(y_test, 10)

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

    def load_cartpole(self):
        # Requires external data
        file_path = "cart_data"

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
        y_train = np_utils.to_categorical(y_train, 10)
        y_test  = np_utils.to_categorical(y_test, 10)

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

    # introduce noise into a test
    def add_noise(self, A, r):
        # Copy, not in place edit
        test = deepcopy(A)

        # Do for both X's
        for i in range(2):
            # For each sample
            for ind,val in enumerate(test[i]):
                # Choose an array of random info of length r
                rans = random.sample(range(0, 1024), r)
                # For each random value
                for j in range(r):
                    # Set random values in 32x32
                    test[i][ind][int(rans[j]/32)][int(rans[j]%32)] = random.random()

        return test

    # p = 1 --> max A
    # p = 0 --> max B
    def join(self, A, B, p):
        # Merged dataset
        data = []

        # For each x,y,train,test
        for ind, val in enumerate(A[0:2]):
            dset_x = []
            dset_y = []

            # For each sample
            for ind2,val2 in enumerate(val):
                r = random.random()

                # For x's
                if r < p:
                    dset_x.append(A[ind][ind2])
                else:
                    dset_x.append(B[ind][ind2])

                # For y's
                if r < p:
                    dset_y.append(list(A[ind+2][ind2]) + [0] * len(B[ind+2][ind2]))
                else:
                    dset_y.append([0] * len(A[ind+2][ind2]) + list(B[ind+2][ind2]))

            # Append set of samples
            data.append(np.asarray(dset_x))
            data.append(np.asarray(dset_y))

        y_tr = data[1]
        data[1] = data[2]
        data[2] = y_tr

        return data




