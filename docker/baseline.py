from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv1D, MaxPooling1D

from keras.utils import np_utils
from keras.datasets import mnist

import time

def gen_model(x,y):
    model = Sequential()
    model.add(Conv1D(8,  kernel_size=(3), activation='relu', input_shape=x.shape))
    model.add(Conv1D(16, kernel_size=(3), activation='relu'))
    model.add(MaxPooling1D(pool_size=(2)))
    model.add(Dropout(0.2))
    model.add(Conv1D(8,  kernel_size=(3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(y, activation='softmax'))
    return mode

## Run Baseline Models and calculate time

# Run MNIST over baseline
(x_train, y_train), (x_test, y_test) = mnist.load_data()


start_time = time.time()



elapsed_time = time.time() - start_time


# Run CIFAR10 over baseline





import csv



x_train = x_train / 255
x_test = x_test / 255

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

'''

def logit(data):
    with open('data_mnist.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(data)
'''

l

model = gen_model(x_train[0], num_classes)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
data = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=50, batch_size=200, verbose=2)

#logit(data.history['val_acc'])

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


