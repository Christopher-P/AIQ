from __future__ import print_function
import vizdoom as vzd

from gym import spaces

import numpy as np
from random import choice
from time import sleep

from PIL import Image

class Env(object):
    
    reward_range = (-300, 200)
    action_space = spaces.Discrete(3)
    observation_space = spaces.Box(0, 255, [120, 160, 3]) 

    def __init__(self, game):
        self.game = game

    def step(self, action):
        take_action = None

        if action == 0:
            take_action = [True, False, False]
        elif action == 1:
            take_action = [False, True, False]
        elif action == 2:
            take_action = [False, False, True]

        reward = self.game.make_action(take_action)
        done = self.game.is_episode_finished()
        if not done:
            state = self.game.get_state().screen_buffer
        else:
            state = np.zeros(shape=(120, 160, 3))
        #info = {"results", "empty"}

        #im = Image.fromarray(np.uint8(state))
        #im = im.resize((40,40))
        #state = np.array(im)
    
        return (state, reward, done, {})


    def reset(self):

        self.game.new_episode()
        state = self.game.get_state().screen_buffer
        #im = Image.fromarray(np.uint8(state))
        #im = im.resize((40,40))
        #state = np.array(im)
        return state

    def render(self, mode='human', close=False):
        return None

    def close(self):

        
        self.game.close()
        return None        

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).
        # Returns
            Returns the list of seeds used in this env's random number generators
        """
        raise NotImplementedError()

    def configure(self, *args, **kwargs):
        """Provides runtime configuration to the environment.
        This configuration should consist of data that tells your
        environment how to run (such as an address of a remote server,
        or path to your ImageNet data). It should not affect the
        semantics of the environment.
        """
        raise NotImplementedError()

    def __del__(self):
        self.close()

    def __str__(self):
        return '<{} instance>'.format(type(self).__name__)

