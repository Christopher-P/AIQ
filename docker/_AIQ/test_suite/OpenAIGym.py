from .common import header
from .common import desc

class OpenAIGym(desc):

    def __init__(self, params):
        # Gives common variables to all environments
        super().__init__()

        try:
            import gym
        except:
            print("Failed to import gym, make sure you have OpenAI gym installed!")
            
        # Handle Parameters
        env_name = params['env_name']

        # Create GYM instance
        self.env = gym.make(env_name)
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

        # Define header
        #TODO: Check all open ai gym envs to see if action space works the same
        #       Workout num_classes based on action_space type
        self.header = header(env_name=env_name, 
                             input_dim=self.observation_space.shape, 
                             output_dim=self.action_space.n,
                             num_classes=2,
                             info="Simulators gotten from OpenAI Gym",
                             env_min_score = 0.0,
                             env_max_score = 200.0,
                             rl=True)

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
        
        
        
