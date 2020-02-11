### Similarity class 
### Will perform a simialrity measure experiment when given two tests
###     Made with respect to the AIQ Framework

import random
import copy 
import numpy as np

### Will perform similarity experiment given two tests
class Similarity():

    ## Accepts two test instances
    def __init__(self, interface, testA=None, testB=None):
        self.testA = testA
        self.testB = testB

        # Setup AIQ system
        self.interface = interface

        # Set our agent
        interface.agent = DQN_Agent()

        return None

    ## Run experiment
    ## P is proportionality split
    def run(self, seed=None, trials=10, p=0.5):
        # check before run
        if self.testA is None or self.testB is None:
            raise Exception ValueError("Tests must be set!")
            return None

        # Create mixed test
        self.testAB = self.join(self.testA, self.testB, p)

        # Get score for A
        score_A = self.interface.fit_to(self.testA)

        # Get score for B
        score_B = self.interface.fit_to(self.testB)

        # Get score for AB
        score_AB = self.interface.fit_to(self.testAB)

        # Get similarity
        sim = self.calc_sim(score_A, score_B, score_AB)

        return score_A, score_B, score_AB, sim
        
    def calc_sim(A, B, AB):
        try:
            sim = (abs(A - AB) - abs(B - AB)) / abs(A - B)
        except Exception as e:
            return -100
        return sim

    ## Used to merge tests utilzing a wrapper
    def join(self, name1, name2, p):
        # Proportion split
        self.p = p

        # TODO: add verbose settings
        print(inst1,inst2)

        # Wrap the test
        wr = wrap(inst1, inst2)
    
        return wr

class wrap():

    def __init__(self, instA, instB, p):
        # Save to local
        self.instA = instA
        self.instB = instB
        self.p
        
        # Proccess test params
        self.instA_in = self.instA.get_header().input_dim
        self.instA_out = self.instA.get_header().output_dim
        self.instB_in = self.instB.get_header().input_dim
        self.instB_out = self.instB.get_header().output_dim

        self.max_in = max(self.instA_in,self.instB_in)
        self.max_out = max(self.instA_out,self.instB_out)
        self.header = header(self.instA.get_header().env_name + "=" +       
                                self.instB.get_header().env_name,
                                self.max_in,
                                self.max_out,
                                -1, "empty", True, -200, 200)

    # random sampling
    def select(self):
        r = random.uniform(0.0, 1.0)
        if r < self.p:
            self.inst = self.instA
        else:
            self.inst = self.instB

    def output_format(self, out):
        if len(out) < self.max_out[0]:
            result = np.zeros(self.max_out[0])
            result[0:len(out)] = out
            #print(out, result)
            return result
        else:
            return out

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


class header():
    
    def __init__(self, env_name, input_dim, output_dim, 
                       info, rl, num_classes=1, 
                       env_min_score=0.0, env_max_score=1.0):

        self.env_name = env_name
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_classes = num_classes
        self.info = info
        self.rl = rl
        self.env_min_score = env_min_score
        self.env_max_score = env_max_score

#EOF
