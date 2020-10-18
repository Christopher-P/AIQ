#!usr/bin/env python3
import random
import numpy as np


# This class takes in two open ai gym envs and creates a new one from them merged
class Merged:

    def __init__(self, instA, instB, p):
        # Save to local
        self.instA = instA
        self.instB = instB
        self.p = p

        # Proccess test params
        self.max_in = max(len(self.instA.actions), len(self.instB.actions))
        dim = []
        for dims in range(3):
            dim.append(max(self.instA.observation_space.shape[dims], self.instB.observation_space.shape[dims]))
        self.max_out = dim
        self.last_out = np.zeros(self.max_out)

    # random sampling
    def select(self):
        r = random.uniform(0.0, 1.0)
        if r < self.p:
            self.inst = self.instA
        else:
            self.inst = self.instB

    def output_format(self, out):
        self.last_out = np.zeros(self.max_out)
        self.last_out[:out.shape[0], :out.shape[1], :out.shape[2]] = out
        return self.last_out

    def input_format(self, inp):
        return inp % self.max_in

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
        # print(self.inst.act(action))
        obs, r, done, info = self.inst.step(action)
        obs = self.output_format(obs)
        return obs, r, done, info

    def render(self):
        return self.inst.render()


