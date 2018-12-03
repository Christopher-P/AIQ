from .common import header
from .common import desc

class MSPackman(desc):

    def __init__(self):
        try:
            # Gives common variables to all environments
            super().__init__()

            try:
                import gym
            except:
                print("Failed to import gym, make sure you have OpenAI gym installed!")
                
            # Define header
            self.header = header(env_name="MSPackman", 
                                 input_dim=10, 
                                 output_dim=10,
                                 info="MSPackman simulator provided by ALE",
                                 rl=True)

            self.env = gym.make("MsPacman-v0")
            self.action_space = self.env.action_space
        except Exception as inst:
            print(inst)

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
        
