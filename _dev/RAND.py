# Out Of The Box solution
# Utilize keras to train and test an agent 
import numpy as np
import random


class RAND_Agent():

    def __init__(self):
        return None

    def fit_to(self, inst):
        self.out_dim = inst.get_header().input_dim

    def test_to(self, inst, iters):
        data = {'episode_reward':[] }
        
        for iteration in range(iters):
            inst.reset()
            done = False
            r_total = None
            while not done:
                action = random.randint(0, self.out_dim - 1)
                obs, r_total, done, info = inst.step(action)

            data['episode_reward'].append(r_total)

        return data

    # Called for RL type tests
    def act(self, header, data):
        if header.info == 'ViZDoom simulator':
            return np.random.choice(2, header.input_dim)
        else:
            size = header.output_dim
            return np.random.choice(header.num_classes, 1)[0]
    
    # Called for DS type tests
    def predict(self, header, data):
        size = header.output_dim
        prediction = []
        for i in data:
            prediction.append(np.random.choice(2, size))
        return prediction

