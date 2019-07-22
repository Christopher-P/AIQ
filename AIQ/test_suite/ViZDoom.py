from .common import header, desc
import numpy as np

class ViZDoom(desc):

    def __init__(self, params):

        super().__init__()
        try:
            import vizdoom
            from argparse import ArgumentParser
        except:
            print("Failed to import ViZDoom, make sure you have ViZDoom installed!")
    
        # Check if config is sent in params
        if 'config' in params:
            DEFAULT_CONFIG = params['config']
        # If not, pull config from env_name
        else:
            file_path = 'AIQ/test_suite/VizDoom/vizdoom_scenarios/'
            # Input --> env_name = vizdoom_stuff_name
            DEFAULT_CONFIG = file_path + params['env_name'] + '.cfg'

        self.env = vizdoom.DoomGame()

        # Incase cfg path is incorrect
        try:
            self.env.load_config(DEFAULT_CONFIG)

        except Exception as inst:
            print(inst)
            print(DEFAULT_CONFIG)
    
        # Define header
        self.header = header(env_name="ViZDoom_" + params['env_name'], 
                             input_dim=len(self.env.get_available_buttons()), 
                             output_dim=[self.env.get_screen_channels(),
                                         self.env.get_screen_height(), 
                                         self.env.get_screen_width(), 
                                         ],
                             info="ViZDoom simulator",
                             env_min_score = -200.0,
                             env_max_score = 100.0,
                             rl=True)

    def get_header(self):
        return self.header
        
    def random_action(self):
        return np.random.choice(2, self.get_header().input_dim)

    # Used for cem agent
    def render(self, mode=None):
        #self.env.render()
        return None

    # Used for CEM Agent
    def step(self, action):
        return self.act(action)

    def act(self, action):
        # Take action
        action = self.decode_action(action)
        self.env.make_action(action)
    
        # Get game state information
        state = self.env.get_state()
        self.observation, 
        self.reward_step = self.env.get_total_reward()
        self.done = self.env.is_episode_finished()
        self.info = ""
        self.reward_step = self.env.get_last_reward()

        if state is not None:
            self.observation = state.screen_buffer / 255

        
        return self.observation, self.reward_step, self.done, {}

    def decode_action(self, action):
        buttons = len(self.env.get_available_buttons())
        response = [False] * buttons
        response[action] = True
        return response
    
    def reset(self):
        
        if not self.init:
            self.env.init()
            self.init = True

        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = False
        self.env.new_episode()

        state = self.env.get_state()
        return state.screen_buffer / 255
