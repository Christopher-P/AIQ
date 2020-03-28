import random
import copy 
import numpy as np
import time


from .common import header

class wrap():

    def __init__(self, instA, instB, p):
        self.p = p
        self.instA = instA
        self.instB = instB
        self.instA_in = self.instA.get_header().input_dim
        self.instA_out = self.instA.get_header().output_dim
        self.instB_in = self.instB.get_header().input_dim
        self.instB_out = self.instB.get_header().output_dim

        self.max_in = self.instA_in + self.instB_in
        self.max_out = max(self.instA_out,self.instB_out)
        self.header = header(self.instA.get_header().env_name + "=" +       
                                self.instB.get_header().env_name,
                                self.max_in,
                                self.max_out,
                                -1, "empty", True, -200, 200)

    def select(self):
        r = random.uniform(0.0, 1.0)
        if r < self.p:
            self.inst = self.instA
            self.current = "A"
        else:
            self.inst = self.instB
            self.current = "B"

    def output_format(self, out):
        if len(out) < self.max_out[0]:
            result = np.zeros(self.max_out[0])
            result[0:len(out)] = out
            return result
        else:
            return out

    def input_format(self, inp):
        #print(self.current)
        #print(inp)
        #time.sleep(1)

        ## If on first inst
        if self.current == "A":
            ## If buttons work on instance (cant use mountaincar buttons on cartpole)
            if inp < self.instA_in:
                return inp
            ## If it doesnt, apply random button press
            ## Because a button needs to pressed, cant press null button
            else:
                inp = random.randint(0, self.instA_in - 1)
                return inp
        else:
            ## If working on second inst, check if cartpole buttons pressed
            if inp < self.instA_in:
                ## If it doesnt, apply random button press
                ## Because a button needs to pressed, cant press null button
                inp = random.randint(0, self.instB_in - 1)
                return inp
            else:
                inp = inp - self.instA_in
                return inp

            
        print(inp)
        return inp
        if inp > self.inst.get_header().input_dim - 1:
            print(self.current)
            print('Correcting')
            return self.inst.get_header().input_dim - 1
        else:
            print(inp)
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

