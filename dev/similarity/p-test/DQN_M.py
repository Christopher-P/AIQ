# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np
import copy 


import keras.backend as K
from keras.layers import Dense, Activation, Flatten, Conv2D, Input, Conv1D, MaxPooling2D, Dropout
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback
from keras.models import Sequential, load_model


from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory, SequentialMemory

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

class DQN_Agent():

    def __init__(self):
        self.ready = False
        return None

    def clear(self):
        self.dqn = None
        self.ready = False

    # k = 100 means normal network
    def fit_to(self, inst, max_val=10):
        k=100
        if not self.ready:
            self.prepare_agent(inst,k)
        train_results = self.dqn.fit(inst, nb_steps=100000, visualize=False, verbose=1)
        return train_results

    def test_to(self, inst, iters):
        data = self.dqn.test(inst, nb_episodes=iters, visualize=False)
        return data

    def gen_model_2D(self, input_dim, output_dim, k):

        ### Format in/out
        input_dim = input_dim[0]
        print(input_dim, output_dim)
        # so shape looks like --> (1, whatever)
        input_dim.insert(0, 50)   
        nb_actions = output_dim   

        # Image classification model
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same',
                         input_shape=(tuple(input_dim))))
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
        model.add(Dense(nb_actions))
        model.add(Activation('softmax'))

        return model

    def gen_model_1D(self, input_dim, output_dim,k):
        model = Sequential()
        #print(input_dim, output_dim)

        # so shape looks like --> (1, whatever)
        inn = copy.deepcopy(input_dim)
        inn.insert(0, 50)        
        #print(tuple(inn))
        print('1 d')
        model.add(Dense(64, input_shape=(tuple(inn))))
        model.add(Conv1D(int(64), 8, strides=2, data_format="channels_last"))
        model.add(Activation('relu'))
        model.add(Conv1D(int(64), 4, strides=2))
        model.add(Activation('relu'))
        model.add(Conv1D(int(64), 2, strides=2))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(int(64)))
        model.add(Activation('relu'))
        model.add(Dense(output_dim[0]))
        model.add(Activation('linear'))

        return model


    def prepare_agent(self, inst,k):
        # Handle Dimensionality  
        in_dim  = inst.get_header().input_dim
        out_dim = inst.get_header().output_dim
        #print(in_dim, out_dim)
        # If dim is int change to list of size 1
        #if type(in_dim) == int:
        #    in_dim = [in_dim]
        #if type(out_dim) == int:
        #    out_dim = [out_dim]

        #if len(in_dim) == 1:
        #    self.model = self.gen_model_1D(out_dim, in_dim,k)
        #elif len(in_dim) == 2:
        #    self.model = self.gen_model_2D(out_dim, in_dim,k)
        self.model = self.gen_model_2D(out_dim, in_dim, k)

        memory = SequentialMemory(limit=50000, window_length=50)
        policy = BoltzmannQPolicy()
        self.dqn = DQNAgent(model=self.model, nb_actions=10, memory=memory, nb_steps_warmup=1000,
                       target_model_update=1e-2, policy=policy)\

        self.dqn.compile(Adam(lr=.00025), metrics=['mae'])

        self.ready = True

        #print(model.summary())






