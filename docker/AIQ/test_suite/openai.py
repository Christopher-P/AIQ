from .util import AIQ
from .Header_def import Header

# Make a generic gym environment!
class OpenAI(AIQ):
    
    def __init__(self, env_name):
        super().__init__()
        try:
            import gym
        except:
            print("Failed to import gym, make sure you have OpenAI gym installed!")
            
        self.env_name = env_name
        self.env = gym.make(env_name)
        self.input_dim = self.env.action_space
        self.output_dim = self.env.observation_space

        self.header = Header(env_name = self.env_name,
                                input_dim = self.input_dim,
                                output_dim = self.output_dim,
                                description = "")
    
    def get_header(self):
        return self.header
        
    def connect(self):
        return super().connect()
        
    def render(self):
        self.env.render()
    
    def act(self, action):
        return super().act(action, self.env_name)
        
    def reset(self):
        super().reset()
        self.env.reset()
        
        
        
