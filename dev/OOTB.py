# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np

import keras.backend as K
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback
from keras.models import Sequential, load_model


from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory



class OOTB_Agent():

    def __init__(self):
        return None

    def fit_to(self, inst):
        self.prepare_agent(inst)
        self.cem.fit(inst, nb_steps=10, visualize=False, verbose=1)

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
        memory = EpisodeParameterMemory(limit=1000, window_length=1)
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
