import yaml
import time
from random import randint

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback, TensorBoard
from keras.models import load_model

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

from numpy import array
import numpy as np

import gym

'''
from test_suite.MSPackman import MSPackMan
from test_suite.CartPole import CartPole
from test_suite.RPM import RPM

from test_suite.benchmark import Benchmark

from test_suite.gen import gen
'''

# RPM STUFF *************************

#https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
def flatten(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list

def genRPM():
    rpm = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    
    #We have three variables in each Matrix
    for i in range(0,3):
        #Start var at a random type (not always blue to start)
        tempVar = randint(0,2) / 2
    
        #Not always increment by type (not blue -> red always)
        if randint(0,1) == 1:
            menter = -1/2
        else:
            menter = 1/2
        
        #Change all columns (accros a row it is the same)
        if randint(0,1) == 1:
            for j in range(0,3):
                #1.1 used to set 1.5 -> 0 so possible choice becomes 0, 0.5, 1.0
                rpm[0 + 3*j][i] = (tempVar + (j * menter))
                rpm[1 + 3*j][i] = (tempVar + (j * menter))
                rpm[2 + 3*j][i] = (tempVar + (j * menter))
        
        #Change all rows
        else:
            for j in range(0,3):
                rpm[0 + j][i] = (tempVar + (j * menter))
                rpm[3 + j][i] = (tempVar + (j * menter))
                rpm[6 + j][i] = (tempVar + (j * menter))
                
        for a in rpm:
            for ind, b in enumerate(a):
                if b > 1.0:
                    a[ind] = 0.0
                if b < 0:
                    a[ind] = 1.0
    
    return rpm
    
def genRPMSet(amount):
    info = []
    solution = []
    rpms = []
    for i in range(0, amount):
        rpm = genRPM()
        if rpm not in rpms:
            rpms.append(rpm)
            #[0:8] because 8 is not included
            info.append(flatten(rpm[0:8]))
            solution.append(rpm[8])
    return (info, solution)

def scoreRPM(x, y):
    runningScore = 0
    maxScore = len(x) * 3
    for set, i in enumerate(x):
        i = i[0]

        #Copy prediction data
        tmpVal = i
        
        #Classify data based on closest prediction
        for ind,val in enumerate(tmpVal):
            
            if val < (1/3):
                tmpVal[ind] = 0.0
            elif val < (2/3) and val >= (1/3):
                tmpVal[ind] = 0.5
            else:
                tmpVal[ind] = 1.0
                
        for ind, j in enumerate(i):
            if j == y[set][0][ind]:
                runningScore += 1
                
    return runningScore / maxScore

# END RPM STUFF **************************


# 



def get_model(input_dim, output_dim):
    model = Sequential()
    i = input_dim
    model.add(Dense(i, input_shape=(1, input_dim), activation='relu'))
    while int(i/10) >= output_dim:
        i = int(i/10)
        model.add(Dense(i, activation='relu'))
        
    model.add(Dense(output_dim, activation='relu'))
    return model


    
import csv

def logit(data, name):
    with open(name, 'a') as f:  # Just use 'w' mode in 3.x
        spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data['val_loss'][1::100])

def logit2(data, name):
    with open(name, 'a') as f:  # Just use 'w' mode in 3.x
        spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data['episode_reward'])


def main():

    #Tensorboard callback
    '''
    # Train and test models on RPM here
    x,y = genRPMSet(1000)
    x = array(x)
    y = array(y)

    #Mean
    for i in range(100):

        model = getMeanModel(24, 3)
        model.compile(loss='mse', optimizer='sgd')

        data = model.fit(x, y, validation_split=0.2, epochs=6000, batch_size=1000)
        logit(data.history, "mean_layer.csv")


    #half
    for i in range(100):

        model = getHalfModel(24, 3)
        model.compile(loss='mse', optimizer='sgd')

        data = model.fit(x, y, validation_split=0.2, epochs=6000, batch_size=1000)
        logit(data.history, "half_layer.csv")


    #tenth
    for i in range(100):

        model = getTenthModel(24, 3)
        model.compile(loss='mse', optimizer='sgd')

        data = model.fit(x, y, validation_split=0.2, epochs=6000, batch_size=1000)
        logit(data.history, "tenth_layer.csv")
    '''
    #**** BEGIN RPM ***** #
    
    ENV_NAME = 'CartPole-v0'

 

    # Get the environment and extract the number of actions.
    env = gym.make(ENV_NAME)
    np.random.seed(14372098)
    env.seed(14372098)

    nb_actions = env.action_space.n
    obs_dim = env.observation_space.shape[0]

    memory = EpisodeParameterMemory(limit=1000, window_length=1)

    #Mean
    tb = TensorBoard(log_dir='./logs/run1/', histogram_freq=0, batch_size=32, write_graph=True, write_grads=False, write_images=False)
    model = get_model(obs_dim, nb_actions)
    cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
                   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
    cem.compile()

    data = cem.fit(env, nb_steps=120000, visualize=False, verbose=1, callbacks=[tb])
    logit2(data.history, 'mean_rpm.csv')
    


    print('Done!')
    exit()
    
    
    
if __name__ == '__main__':
    main()
    
