# Make a ViZDoom class (to be tested on linux system, windows is meh for it)
class ViZDoom(AIQ):
	def __init__(self):
		super().__init__()
		try:
			import ViZDoom
		except:
			print("Failed to import ViZDoom, make sure you have ViZDoom installed!")
			
	
	#def get_header(self):
		
		
	def connect(self):
		return super().connect()
		
	def render(self):
		self.env.render()
	
	def act(self, action):
		return super().act(action, 'CartPole-v0')
		
	def reset(self):
		super().reset()
		self.env.reset()


