#/usr/bin/env python3
from PIL import Image

from keras.utils import np_utils
from keras.datasets import cifar10, cifar100, mnist, fashion_mnist

from os import listdir
from os.path import isfile, join

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
        ''' # not needed after switch to npy save!
        ### Load image data (x)
        x = []

        # Requires external data
        file_path = "cart_data"

        # Get all files in dir
        onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]

        # Sort according to file name (0.png --> 1.png --> ...)
        onlyfiles = sorted(onlyfiles, key = lambda x: int(x.split('.')[0]))

        # Load images into array
        for entry in onlyfiles:
            entry_dat = np.array(Image.open(file_path + '/' + entry))
            x.append(entry_dat)

        # Convert to greyscale, normalize
        rgb_convert = [0.2989,0.5870,0.1140]
        x = np.dot(x, rgb_convert)/255
        x = np.subtract(1,x)

        # Conver to correct shape (n,x,y,1)
        x = np.reshape(x,(60000, 32,32,1))
       
        ### Load correct action (y)
        y  = np.load('actions.npy')
        
        # Convert to one-hot
        y = np_utils.to_categorical(y, 2)

        ## Save unique x,y to pkl
        ### TMP, remove later
        unique = set()
        x_save = []
        y_save = []
        for ind,val in enumerate(x):
            hashed = hash(x[ind].data.tobytes() ) 
            if hashed in unique:
                continue
            else:
                unique.add(hashed)
                x_save.append(x[ind])
                y_save.append(y[ind])

        x_save = np.asarray(x_save)
        y_save = np.asarray(y_save)

        np.save('cart_x.npy', x_save)
        np.save('cart_y.npy', y_save)
        exit()
        '''     

        ''' # Convert 6 npy files into one file
        y = []
        x = []        

        for i in range(6):
            y.append(np.load('actions_' + str(i) + '.npy'))
            x.append(np.load('observations_' + str(i) + '.npy'))

        x = np.reshape(x, (60000, 32, 32))
        y = np.reshape(y, (60000, -1))

        print(x[0])
        print(y[0])
        print(x.shape)
        print(y.shape)
        
        np.save('actions.npy', y)
        np.save('cart_data.npy', x)

        exit()
        '''

        # Load from save
        x = np.load('cart_x.npy')
        y = np.load('cart_y.npy')

        # Correct shape
        x = np.reshape(x, (60000, 32, 32, 1))
        y = np_utils.to_categorical(y, 2)

        print(x.shape)
        print(y.shape)

        ### Split into train/test
        x_train = x[0:50000]
        x_test  = x[50000:]
        y_train = y[0:50000]
        y_test  = y[50000:]

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
        y_train = np_utils.to_categorical(y_train, 10)
        y_test  = np_utils.to_categorical(y_test, 10)

        # Reduce sizes to 50k
        x_train = x_train[0:50000]
        x_test  = x_test[0:50000]
        y_train = y_train[0:50000]
        y_test  = y_test[0:50000]

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
        if np.array_equal(np.asarray(A), np.asarray(B)):
            print('Same test detected!')
            return A
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

                # Set marker pixel
                if r < p:
                    dset_x[-1][0] = 1.0
                else:
                    dset_x[-1][0] = 0.0

            # Append set of samples
            data.append(np.asarray(dset_x))
            data.append(np.asarray(dset_y))

        y_tr = data[1]
        data[1] = data[2]
        data[2] = y_tr

        return data




