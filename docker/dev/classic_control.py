# Implemention of random agent
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv1D, MaxPooling1D, Reshape, Dropout
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback, TensorBoard
from keras.models import load_model
from keras.utils import to_categorical
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory


import keras.backend as K

class Agent():

    # Find manualy from test suite
    self.max_obs = 10
    self.max_act = 10

    def __init__(self):
        self.NN = model(self.max_obs, self.max_act)
        return None

    # Called for RL type tests
    def act(self, header, data):
        
    
    # Called for DS type tests
    # Not needed for classic_control only
    def predict(self, header, data):
        return None

    # Pads input with zero
    # TODO: Evenly space inputs
    def fill_input(self, inputs):
        return None

    def norm_obs(self, obs, header):
        high = header.output_dim.high
        low = header.output_dim.low
        
        for ind, val in enumerate(obs):
            obs[ind] = (val - low[ind]) / (high[ind] - low[ind])
        
        return obs

    def make_NN(self, input_size, output_size):
        model = Sequential()
        model.add(Conv1D(8, kernel_size=(3),activation='relu',input_shape=(input_size,1)))
        model.add(Conv1D(8, kernel_size=(3),activation='relu'))
        model.add(MaxPooling1D(pool_size=(2)))
        model.add(Dropout(0.2))
        model.add(Flatten())
        model.add(Dense(8, activation='relu'))
        model.add(Dense(6, activation='softmax'))
        model.add(Dense(output_size, activation='softmax'))

        memory = EpisodeParameterMemory(limit=1000, window_length=1)
		self.cem = CEMAgent(model=model, nb_actions=nb_actions, 
                        memory=memory,batch_size=50, nb_steps_warmup=2000, 
                        train_interval=50, elite_frac=0.05)
		self.cem.compile()
        
