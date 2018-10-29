from .util import AIQ

# Make a cartpole AIQ class!
class MSPackMan(AIQ):
    
    def __init__(self):
        super().__init__()
        try:
            import gym
        except:
            print("Failed to import gym, make sure you have OpenAI gym installed!")
            
        self.env = gym.make('Acrobot-v1')
        self.action_space = self.env.action_space
    
    def get_header(self):
        print("hello world")
        
    def connect(self):
        return super().connect()
        
    def render(self):
        self.env.render()
    
    def act(self, action):
        return super().act(action, 'Acrobot-v1')
        
    def reset(self):
        super().reset()
        self.env.reset()
        
        