class AIQ():

	def __init__(self, env):
		self.env = env
		self.observation = None
		self.reward = None
		self.done = None
		self.info = None
		self.password = None
		self.username = None
		
	def reset(self):
		self.env.reset()
	
	def act(self, action):
		self.observation, self.reward, self.done, self.info = self.env.step(action)
	
	def render(self):
		self.env.render
		
	def connect(self):
		# TODO
		return None
		
	def get_env(self):
		return sefl.env