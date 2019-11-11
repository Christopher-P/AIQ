# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np

import keras.backend as K
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback, EarlyStopping
from keras.models import Sequential, load_model

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

class epoch_check(Callback):

    def __init__(self, cutoff):
        self.cutoff = float(cutoff)

    def on_episode_end(self, episode, logs=None):
        #print("Epoch : ", episode)
        #print("Logs : ", logs)
        #print("HERE:", logs['episode_reward'], self.cutoff)
        if logs['episode_reward'] > self.cutoff:
            self.model.step = 9999999999999999

class C_Agent():

    def __init__(self):
        return None

    def train(self):
        # Set new agent
        self.agent = OOTB_Agent()

        # Train new agent
        e = self.agent.fit_to(self.inst)

        # get tp and ntp
        tp, ntp = self.agent.get_params()
        
        return e, tp, ntp

    def reset(self, inst):
        self.inst = inst
        self.agent = None
        return None

class OOTB_Agent():

    def __init__(self):
        
        return None

    def get_params(self):
        trainable_count = int(
            np.sum([K.count_params(p) for p in set(self.cem.model.trainable_weights)]))
        non_trainable_count = int(
            np.sum([K.count_params(p) for p in set(self.cem.model.non_trainable_weights)]))
        return trainable_count, non_trainable_count

    def clear(self):
        self.cem = None

    def fit_to(self, inst):
        self.prepare_agent(inst)
        # Set callback functions to early stop training and save the best model so far
        callbacks = [epoch_check(190)]
        hist = self.cem.fit(inst, nb_steps=1000000, visualize=False, verbose=1, callbacks=callbacks)
        
        # Retreive e
        e = hist.epoch[-1]

        return e

    def test_to(self, inst, iters):
        data = self.cem.test(inst, nb_episodes=iters, visualize=False)
        return data

    def gen_model(self, input_dim, output_dim):
        model = Sequential()
        print(input_dim, output_dim)

        # so shape looks like --> (1, whatever)
        input_dim.insert(0, 1)        
        print(tuple(input_dim))
        
        model.add(Dense(16, input_shape=(tuple(input_dim)) ))
        model.add(Flatten())

        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(output_dim[0]))
        model.add(Activation('softmax'))
        model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

        return model


    def prepare_agent(self, inst):
        # Handle Dimensionality  
        in_dim  = inst.get_header().input_dim
        out_dim = inst.get_header().output_dim

        # If dim is int change to list of size 1
        if type(in_dim) == int:
            in_dim = [in_dim]
        if type(out_dim) == int:
            out_dim = [out_dim]

        model = self.gen_model(out_dim, in_dim)
        memory = EpisodeParameterMemory(limit=5000, window_length=1)
        cem = CEMAgent(model=model, 
                       nb_actions=in_dim[0], 
                       memory=memory,
                       batch_size=50, 
                       nb_steps_warmup=1000, 
                       train_interval=50, 
                       elite_frac=0.05)
        cem.compile()
        self.cem = cem
        print(model.summary())


