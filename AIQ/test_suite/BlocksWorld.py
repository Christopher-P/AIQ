from .common import header, desc

from blocks_world_data.generator import Simulator

class BlocksWorld(desc):
        
    def __init__(self, params):
        try:
            super().__init__()
            self.header = header(env_name="BlocksWorld", 
                                 input_dim=24, 
                                 output_dim=3,
                                 info="",
                                 rl=False)

        except Exception as inst:
            print(inst)

        if 'blocks' in params:
            blocks = params['blocks']
        else:
            blocks = 5
    
        if 'size' in params:
            size = params['size']
        else:
            size = 5

        if 'limit' in params:
            limit = params['limit']
        else:
            limit = 2000

        self.env = Simulator(size, blocks, None, limit)

    
    def get_header(self):
        return self.header
        
    def render(self, mode=None):
        return None
    
    def act(self, action):
        self.obs = self.env.act(action)  
        return self.env.obs(), self.env.score(), self.env.is_done, None     

    # Used for cem agent
    def step(self, action):
        return self.act(action)
        
    def reset(self):
        self.obs = self.env.reset()
        return self.env.obs(), self.env.score(), self.env.is_done, None
        
        
