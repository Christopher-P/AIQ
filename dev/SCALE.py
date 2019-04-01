# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np
import math

import keras.backend as K
from keras.layers import Dense, Activation, Flatten, Conv1D, Conv2D, MaxPooling1D, MaxPooling2D, Dropout
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback
from keras.models import Sequential, load_model


from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory



class SCALE_Agent():

    def __init__(self):
        return None

    def clear(self):
        self.cem = None

    def fit_to(self, inst):
        self.prepare_agent(inst)
        self.cem.fit(inst, nb_steps=100000, visualize=False, verbose=1)

    def test_to(self, inst, iters):
        data = self.cem.test(inst, nb_episodes=iters, visualize=False)
        return data
    # https://stackoverflow.com/questions/14267555/find-the-smallest-power-of-2-greater-than-n-in-python
    def next_power_of_2(self, x):
        x = x[0]
        return 1 if x == 0 else 2**math.ceil(math.log2(x))

    def log_finder(self, x):
        n = 1
        if len(x.shape) == 1:
            n = x.shape[0]
        if len(x.shape) == 2:
            n = x.shape[0] * x.shape[1]
        if len(x.shape) == 3:
            n = x.shape[0] * x.shape[1] * x.shape[2]
        if n <= 1:
            n = 2
        
        return int(math.ceil(math.log(n)))

    def gen_model(self, input_dim, output_dim):
    
        #print(tuple(input_dim))
        print('gen model: ', input_dim, output_dim)
        sh = np.array(input_dim)

        # so shape looks like --> (1, whatever)
          

        # get log of sum of input dims
        dim = self.log_finder(sh)
        print(dim)
        input_dim.insert(0, 1)  
        model = Sequential()

        if len(sh) == 1:
            
            # Build up shape
            for i in range(dim):
                if i == 0:
                    model.add(Dense(8 * int(math.pow(2, i)), activation='relu', input_shape=(tuple(input_dim))))

                else:
                    model.add(Dense(8 * int(math.pow(2, i)), activation='relu'))
            # Build down shape
            for i in range(dim, -1, -1):
                model.add(Dense(8 * int(math.pow(2, i)), activation='relu'))

        if len(sh) == 2:

            # Build up shape
            for i in range(dim):
                if i == 0:
                    model.add(Conv1D(8 * int(math.pow(2, i)), kernel_size=(3), activation='relu', input_shape=(tuple(input_dim))))
                else:
                    model.add(Conv1D(8 * int(math.pow(2, i)), kernel_size=(3), activation='relu'))
                if i % 2 == 0 and i > 0:
                    model.add(MaxPooling1D(pool_size=(2)))
                    model.add(Dropout(0.2))

            # Build down shape
            for i in range(dim, -1, -1):
                model.add(Conv1D(8 * int(math.pow(2, i)), kernel_size=(3), activation='relu'))
                if i % 2 == 0 and i > 0:
                    model.add(MaxPooling1D(pool_size=(2)))
                    model.add(Dropout(0.2))

            model.add(Flatten())

        if len(sh) == 3:
            
            # Build up shape
            for i in range(dim):
                if i == 0:
                    model.add(Conv2D(8 * int(math.pow(2, i)), kernel_size=(3), activation='relu', input_shape=(tuple(input_dim))))
                else:
                    model.add(Conv2D(8 * int(math.pow(2, i)), kernel_size=(3), activation='relu'))
                if i % 2 == 0 and i > 0:
                    model.add(MaxPooling2D(pool_size=(2)))
                    model.add(Dropout(0.2))

            # Build down shape
            for i in range(dim, -1, -1):
                model.add(Conv2D(8 * int(math.pow(2, i)), kernel_size=(3), activation='relu'))
                if i % 2 == 0 and i > 0:
                    model.add(MaxPooling2D(pool_size=(2)))
                    model.add(Dropout(0.2))

            model.add(Flatten())

        # 2 power of twos bigger than output
        n = self.next_power_of_2(output_dim)

        model.add(Dense(n * 4, activation='relu'))
        model.add(Dense(n * 2, activation='relu'))

        model.add(Dense(output_dim[0], activation='softmax'))
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
