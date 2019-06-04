from ..common import header, desc

import numpy as np
import random

class OTB(desc):

    def __init__(self, params):
        # Gives common variables to all environments
        super().__init__()

        try:
            from obstacle_tower_env import ObstacleTowerEnv
        except:
            print("Failed to import ObstacleTowerEnv, make sure you have Obstacle Tower installed!")
            
        # Handle Parameters
        env_name = params['env_name']

        # Create GYM instance
        env = ObstacleTowerEnv('./ObstacleTower/obstacletower', retro=False)
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

        # Store for later
        self.disc = gym.spaces.discrete.Discrete

        # Define header
        #TODO: Check all open ai gym envs to see if action space works the same
        #       Workout num_classes based on action_space type
        if type(self.observation_space) == self.disc:
            self.out = [self.observation_space.n]
        else:
            self.out = list(self.observation_space.shape)

        self.header = header(env_name=env_name, 
                             input_dim=self.action_space.n,
                             output_dim=self.out, 
                             num_classes=2,
                             info="",
                             env_min_score = 0.0,
                             env_max_score = 200.0,
                             rl=True)

    def get_header(self):
        return self.header
        
    def render(self, mode=None):
        self.env.render()
    
    def act(self, action):
        self.observation, self.reward_step, self.done, self.info = self.env.step(action)
        self.reward_total += self.reward_step
        self.steps += 1
        if self.steps >= 2000:
            self.done = True
        
        # Only show screen atm
        # TODO: think of good way to send screen and keys obs
        self.observation = self.observation[0] / 255

        if self.done:
            return self.observation, self.reward_total, self.done, self.info
        else:
            return self.observation, self.reward_step, self.done, self.info

    # Used for cem agent
    def step(self, action):
        return self.act(action)
        
    def reset(self):
        self.steps = 0
        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = False
        self.observation = self.env.reset()


        self.observation = self.observation[0] / 255

        return self.observation
        
        
