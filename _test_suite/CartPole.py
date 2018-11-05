from .util import AIQ

# Make a cartpole AIQ class!
class CartPole(AIQ):
    
    def __init__(self):
        super().__init__()
        try:
            import gym
        except:
            print("Failed to import gym, make sure you have OpenAI gym installed!")
            
        self.env = gym.make('CartPole-v0')
        self.action_space = self.env.action_space
    
    def get_header(self):
        print("hello world")
        
    def connect(self):
        return super().connect()
        
    def render(self):
        self.env.render()
    
    def act(self, action):
        return super().act(action, 'CartPole-v0')
        
    def reset(self):
        super().reset()
        self.env.reset()
        
        
        