# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np
import copy 


import keras.backend as K
from keras.layers import Dense, Activation, Flatten, Conv2D, Input, Conv1D
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

class AtariProcessor(Processor):
    def process_observation(self, observation):
        #assert observation.ndim == 3  # (height, width, channel)
        #img = Image.fromarray(observation)
        #img = img.resize(INPUT_SHAPE).convert('L')  # resize and convert to grayscale
        processed_observation = np.array(observation)
        #assert processed_observation.shape == INPUT_SHAPE
        return processed_observation.astype('uint8')  # saves storage in experience memory

    def process_state_batch(self, batch):
        # We could perform this processing step in `process_observation`. In this case, however,
        # we would need to store a `float32` array instead, which is 4x more memory intensive than
        # an `uint8` array. This matters if we store 1M observations.
        #print(type(batch))
        #print(batch)
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return np.clip(reward, -200., 200.)

class DQN_Agent():

    def __init__(self):
        return None

    def clear(self):
        self.dqn = None

    def fit_to(self, inst):
        self.prepare_agent(inst)
        train_results = self.dqn.fit(inst, nb_steps=20000, visualize=False, verbose=1)
        return train_results

    def test_to(self, inst, iters):
        data = self.dqn.test(inst, nb_episodes=iters, visualize=False)
        return data

    def gen_model_2D(self, input_dim, output_dim):
        model = Sequential()
        #print(input_dim, output_dim)

        # so shape looks like --> (1, whatever)
        input_dim.insert(0, 32)        
        #print(tuple(input_dim))
        
        model.add(Conv2D(32, (8, 8), strides=(4, 4), input_shape=(tuple(input_dim))))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (4, 4), strides=(2, 2)))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3), strides=(1, 1)))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dense(nb_actions))
        model.add(Activation('softmax'))

        return model

    def gen_model_1D(self, input_dim, output_dim):
        model = Sequential()
        #print(input_dim, output_dim)

        # so shape looks like --> (1, whatever)
        inn = copy.deepcopy(input_dim)
        inn.insert(0, 500)        
        #print(tuple(inn))
        
        model.add(Dense(16, input_shape=(tuple(inn))))
        model.add(Conv1D(64, 8, strides=2, data_format="channels_last"))
        model.add(Activation('relu'))
        model.add(Conv1D(64, 4, strides=2))
        model.add(Activation('relu'))
        model.add(Conv1D(64, 2, strides=2))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dense(output_dim[0]))
        model.add(Activation('linear'))

        return model


    def prepare_agent(self, inst):
        # Handle Dimensionality  
        in_dim  = inst.get_header().input_dim
        out_dim = inst.get_header().output_dim
        #print(in_dim, out_dim)
        # If dim is int change to list of size 1
        if type(in_dim) == int:
            in_dim = [in_dim]
        if type(out_dim) == int:
            out_dim = [out_dim]

        if len(in_dim) == 1:
            model = self.gen_model_1D(out_dim, in_dim)
        elif len(in_dim) == 2:
            model = self.gen_model_2D(out_dim, in_dim)

        memory = SequentialMemory(limit=10000, window_length=500)
        processor = AtariProcessor()
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=200., 
                    value_min=-200., value_test=.05, nb_steps=1000000)

        self.dqn = DQNAgent(model=model, nb_actions=in_dim[0], policy=policy, memory=memory,
                       processor=processor, nb_steps_warmup=1000, 
                       gamma=.99, target_model_update=10000,
                       train_interval=4, delta_clip=1.)

        self.dqn.compile(Adam(lr=.00025), metrics=['mae'])



        print(model.summary())
