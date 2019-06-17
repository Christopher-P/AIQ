import random
import copy 
import numpy as np
import time

from .common import header

class wrap():

    def __init__(self, instA, instB):
        self.instA = instA
        self.instB = instB
        self.instA_in = self.instA.get_header().input_dim
        self.instA_out = self.instA.get_header().output_dim
        self.instB_in = self.instB.get_header().input_dim
        self.instB_out = self.instB.get_header().output_dim

        self.max_in = max(self.instA_in,self.instB_in)
        # Expect shape = [a,b,c]
        # Expect same dims between instances
        self.max_out = []
        for ind, val in enumerate(self.instA_out):
            self.max_out.append(max(self.instA_out[ind],self.instB_out[ind]))

        self.header = header(self.instA.get_header().env_name + "=" +       
                                self.instB.get_header().env_name,
                                self.max_in,
                                self.max_out,
                                -1, "empty", True, -200, 200)

    def select(self):
        r = random.uniform(0.0, 1.0)
        if r < 0.5:
            self.inst = self.instA
        else:
            self.inst = self.instB

    def output_format(self, out):
        big_out = np.zeros(self.max_out)
        big_out[0:out.shape[0], 0:out.shape[1], 0:out.shape[2]] = out
        return big_out

    def input_format(self, inp):
        if inp > self.inst.get_header().input_dim - 1:
            return self.inst.get_header().input_dim - 1
        else:
            return inp

    def reset(self):
        self.select()
        obs = self.inst.reset()
        obs = self.output_format(obs)
        return obs

    # Calls act 
    def step(self, action):
        return self.act(action)

    def act(self, action):
        action = self.input_format(action)
        #print(self.inst.act(action))
        obs, r, done, info = self.inst.act(action)
        obs = self.output_format(obs)
        return obs, r, done, info 

    def render(self):
        return self.inst.render()
    
    def get_header(self):
        return self.header

