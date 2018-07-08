import json
import requests
from threading import Thread, Lock

# Not designed to do much
# Will serve as a parent for other classes to inherent from
class AIQ():

	def __init__(self):

		# Not dependent on a specific envrionment
		self.observation = None
		self.reward_step = 0
		self.reward_total = 0
		self.done = None
		self.password = None
		self.username = None
		self.updating = False

		# Used so we can send batches of data updates to aiq
		self.mutex = Lock()
		self.update_amt = 0
		
		# TODO
		# Make verbose options
		print("done")
		
	# Reset the environment
	def reset(self):
		self.observation = None
		self.reward_step = 0
		self.reward_total = 0
		self.done = False
		self.env.reset()
		
	# Utility function for sending batch of data
	def update(self, env_name):
		
		#Lock in-case of poor threading
		self.mutex.acquire()
		try:
			if(self.update_amt == 0):
				return None
				
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : update_amt,
				"test_name" : env_name
			}
			# TODO 
			# Make verbose option
			print(requests.post(url, data=json.dumps(data)), self.update_amt)
			
		finally:
			self.updating = False
			self.update_amt = 0
			self.mutex.release()
	
	def act(self, action, env_name):
		
		# Whenever act gets called, increment update amount by one
		# TODO
		# Add separate metric for number of env calls (not just step based)
		self.update_amt += 1
		
		# Begin thread to send of batch of data
		if(self.updating == False):
			self.updating = True
			Thread(target=self.update).start()
		
		#Update information based on results of action
		self.observation, self.reward_step, self.done, self.info = self.env.step(action)
		self.reward_total += self.reward_step
		
	#Return true if connection and credentials are good
	def connect(self):
		url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
		data = {
			"username"  : self.username,
			"password"  : self.password,
			"data"      : 1,
			"test_name" : "Connect"
		}
		results = requests.post(url, data=json.dumps(data))
		#print(results.text)
		if(results.text == '\"Connection Successful\"'):
			return True
		else:
			return False
		
	def get_env(self):
		return self.env
		

# Make a cartpole AIQ class!
class CartPole(AIQ):
	
	def __init__(self):
		super().__init__()
		import gym
		self.env = gym.make('CartPole-v0')
		self.action_space = self.env.action_space
	
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
		
		
# Make a ViZDoom class (to be tested on linux system, windows is meh for it)
#class ViZDoom(AIQ):
	
	

#class RPM(AIQ):


