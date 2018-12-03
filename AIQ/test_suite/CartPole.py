from .common import header
from .common import desc

class CartPole(desc):

    def __init__(self):
        # Gives common variables to all environments
        super().__init__()

        try:
            import gym
        except:
            print("Failed to import gym, make sure you have OpenAI gym installed!")
            
        # Define header
        self.header = header(env_name="CartPole", 
                             input_dim=10, 
                             output_dim=10,
                             info="CartPole simulator provided by OpenAI",
                             rl=True)

        self.env = gym.make('CartPole-v0')
        self.action_space = self.env.action_space

    def get_header(self):
        return self.header

        
    def render(self):
        self.env.render()
    
    def act(self, action):
        self.observation, self.reward_step, self.done, self.info = self.env.step(action)
        self.reward_total += self.reward_step
        
    def reset(self):
        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = False
        self.env.reset()
        
        
        
