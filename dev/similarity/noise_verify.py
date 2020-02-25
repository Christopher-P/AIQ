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

# Import similarity util
from sim_util import Similarity

## Experiment parameters
seed = 123
proportion = 0.5
trials = 10
# p = 0.0 --> all B, p = 1.0 --> all A
## End parameters

def logger(Aname, Bname, A, B, AB, S, seed, trials, proportion):
    with open('./dev/similarity/r-noise.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([Aname, Bname, A, B, AB, S, seed, trials, proportion])
    return None

def gen_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=x_train.shape[1:]))
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
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    return model

def main():
    global seed
    global proportion
    global trials

    ### Create AIQ interface
    interface = AIQ("","")

    ### Add classification test
    names = {'CIFAR10':{'env_name':'CIFAR10'},
             'CIFAR10_r':{'env_name':'CIFAR10_r'}}
    for i in names.keys():
        interface.add(i, names[i])

    ### Setup 
    #sim_backend = Similarity(interface)
    
    ### Load data       
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    # Normalize xs
    x_train = x_train / 255
    x_test = x_test / 255

    # Convert to greyscale
    rgb_convert = [0.2989,0.5870,0.1140]
    x_train = np.dot(x_train, rgb_convert)
    x_test  = np.dot(x_test , rgb_convert)

    y_train = np_utils.to_categorical(y_train)
    y_test =  np_utils.to_categorical(y_test)

    ## Run experiment
    for i in range(10):
        
        # set num of pixels to replace with noise
        sim_backend.testB.r = i
        sim_backend.testB.regen()
        
        # Run it
        A,B,AB,S = sim_backend.run(seed=seed,trials=trials,p=proportion)

        # Log it
        testA_name = 'CIFAR10'
        testB_name = 'CIFAR10_r' + str(i)
        logger(testA_name, testB_name, A, B, AB, S, seed, trials, proportion)

        # Reset agent (prevent any TL)
        interface.agent.clear()



if __name__ == "__main__":
    main()
