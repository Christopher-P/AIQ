from .common import header
from .common import desc

class ALE(desc):

    def __init__(self, params):
        try:
            # Gives common variables to all environments
            super().__init__()

            try:
                import gym
                
                all_envs = gym.envs.registry.all()
                env_ids = [env_spec.id for env_spec in all_envs]
                if 'MsPacman-v0' not in env_ids:
                    print("OpenAI GYM found but ALE not found!")
                    raise Exception('ALE NOT FOUND!')
                
            except:
                print("""Failed to import gym / ALE, make sure you have
                         OpenAI gym installed and atari dependencies!""")
            # Handle Parameters
            env_name = params['env_name']
            name = params['name']
            # Create ALE instance
            self.env = gym.make(env_name)
            self.action_space = self.env.action_space
            self.observation_space = self.env.observation_space
  
            # Define header
            self.header = header(env_name=name, 
                                 input_dim=self.action_space, 
                                 output_dim=self.observation_space,
                                 info="Simulators gotten from ALE",
                                 rl=True)

        # Handle unkown bugs
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
        
