class CartPole_new():

    def __init__(self):
        # Initial setup
        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = None
        self.results = []
        self.info = None
        self.name = "CartPole"
        self.rl = True

        try:
            import gym
        except:
            print("Failed to import gym, make sure you have OpenAI gym installed!")
            
        self.env = gym.make('CartPole-v0')
        self.action_space = self.env.action_space

    
        #self.header = Header(env_name = 'CartPole-v0')
    
    def get_header(self):
        print("hello world")

        
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
        
        
        
