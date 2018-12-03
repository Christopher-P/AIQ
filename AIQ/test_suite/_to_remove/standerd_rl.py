from .util import AIQ
from .util import Header

class ClassName(AIQ):
    
    def __init__(self):
        super().__init__()
        try:
            # Locate external files / environments here
        except:
            # print("Unable to find environment!")
         
        # Define the environment
        #self.env = 
        #self.action_space = self.env.action_space
        self.header = Header('env', 0, 0, 'env desc')
    
    def get_header(self):
        return self.header
        
    def connect(self):
        return super().connect()
        
    # If env object has rendering capabilities
    def render(self):
        #self.env.render()
    
    def act(self, action):
        #return super().act(action, 'CartPole-v0')
        
    def reset(self):
        #super().reset()
        #self.env.reset()
        