# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np

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
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return np.clip(reward, -200., 200.)

class DQN_Agent():

    def __init__(self, n):
        self.hand = n
        self.compiled = False
        return None

    def clear(self):
        self.dqn = None

    def gen_model_1D(self, input_dim, output_dim):
        k = self.hand
        model = Sequential()
        #print(input_dim, output_dim)

        # so shape looks like --> (1, whatever)
        #input_dim = [15,500]    
        #print(tuple(input_dim))
        input_shape = (1,10)
        model.add(Dense(int(10 * k / 100) + 1, input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(Dense(int(10 * k / 100) + 1))
        model.add(Activation('relu'))
        model.add(Dense(int(10 * k / 100) + 1))
        model.add(Flatten())
        model.add(Dense(5))
        model.add(Activation('linear'))

        print(model.summary())
        return model


    def prepare_agent(self, inputs, outputs):
        if self.compiled:
            return None

        # Handle Dimensionality  
        in_dim  = inputs
        out_dim = outputs

        #print(in_dim, out_dim)
    
        model = self.gen_model_1D(in_dim,out_dim)
        print("MODEL")
        memory = SequentialMemory(limit=50000, window_length=10)
        policy = BoltzmannQPolicy()
        self.dqn = DQNAgent(model=model, nb_actions=in_dim[0], memory=memory, nb_steps_warmup=10,
                       target_model_update=1e-2, policy=policy)

        print("DQQN")
        try:
            self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])
        except Exception as e:
            print(e)
        print("COMP")
        self.compiled = True




