from .common import header
from .common import desc

import numpy as np

class ViZDoom(desc):

    def __init__(self, params):

        super().__init__()
        try:
            import vizdoom
            from argparse import ArgumentParser
        except:
            print("Failed to import ViZDoom, make sure you have ViZDoom installed!")
    

        DEFAULT_CONFIG = params['config']
        self.env = vizdoom.DoomGame()

        # Incase cfg path is incorrect
        try:
            self.env.load_config(DEFAULT_CONFIG)
        except Exception as inst:
            print(inst)
            print(DEFAULT_CONFIG)
    
        # Define header
        self.header = header(env_name="ViZDoom", 
                             input_dim=len(self.env.get_available_buttons()), 
                             output_dim=[self.env.get_screen_height(), 
                                         self.env.get_screen_width(), 
                                         self.env.get_screen_channels()],
                             info="ViZDoom simulator (rawr)",
                             rl=True)

    def get_header(self):
        return self.header
        
    def random_action(self):
        return np.random.choice(2, self.get_header().input_dim)

    def render(self):
        self.env.render()
    
    def act(self, action):
        # Take action
        self.env.make_action(list(action))
    
        # Get game state information
        state = self.env.get_state()
        self.observation, 
        self.reward_step = self.env.get_total_reward()
        self.done = self.env.is_episode_finished()
        self.info = ""
        self.reward_total = self.reward_step
        
    def reset(self):
        if not self.init:
            self.env.init()
            self.init = True

        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = False
        self.env.new_episode()
