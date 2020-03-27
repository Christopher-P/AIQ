import csv
import statistics 

import keras.backend as K
from keras.layers import Dense, Activation, Flatten, Conv2D, Input, Conv1D, Conv3D, MaxPooling2D, Dropout, Reshape
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback
from keras.models import Sequential, load_model

from test_gen import test, join

# generates a list of all pairwise combinations
def get_list(tests):

    real_names = []

    for ind,val in enumerate(tests):
        for ind2,val2 in enumerate(tests):
            if ind2 < ind:
                continue
            real_names.append((val, val2))

    return real_names


def loggit(name, results, file_name='all_test_data-3000', write='a'):
    res = results.history['val_mean_absolute_error'][-5:]

    # res is mae, not accuracy --> goto accuracy
    for ind, val in enumerate(res):
        res[ind] = 1.0 - val

    with open(file_name + '.csv', write, newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        avg = sum(res) / len(res)
        stdev = statistics.stdev(res)
        spamwriter.writerow((name, len(res), avg, -1*stdev, stdev, *res))

def run_b(s_test):
    model = gen_model(3000, 1)
    model.compile(optimizer='adam',loss='mse',metrics=['MAE'])

    # train a
    model.reset_states()
    x,y = s_test.sample_n(10000)
    hist = model.fit(x,y,epochs=15, verbose=1, validation_split=0.2)
    loggit(s_test.name, hist)

def run(p_test):
    a,b = p_test
    c = join(a,b)

    model = gen_model(3000, 1)
    model.compile(optimizer='adam',loss='mse',metrics=['MAE'])

    # train c
    model.reset_states()
    x,y = c.sample_n(10000)
    hist = model.fit(x,y,epochs=15, verbose=1, validation_split=0.2)
    loggit(c.name, hist)

def gen_model(inp, out):
    model = Sequential()
    model.add(Dense(32, input_shape=(3000,)))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(8))
    model.add(Activation('relu'))
    model.add(Dense(4))
    model.add(Activation('relu'))
    model.add(Dense(out))
    model.add(Activation('tanh'))
    return model

def main():
    # create list of tests
    tests = []
    for i in range(20):    
        tests.append(test(3000,i))

    # create a pair-wise list of that list of tests
    pair_wise = get_list(tests)

    # run a single baseline for each test
    for i in tests:
        run_b(i)

    # run agent over a,b,c in pairwise
    for i in pair_wise:
        run(i)
    



if __name__ == "__main__":
    main()


