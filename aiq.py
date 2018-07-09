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
		self.log = False
		self.results = []
		
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
		self.log_res = True
		self.env.reset()
		
	# Utility function for sending batch of data
	def update_aiq(self):
		print("updating")
		try:
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : self.update_amt,
				"test_name" : "CartPole-v0"
			}
			# TODO 
			# Make verbose option
			self.update_amt = 0
			print(requests.post(url, data=json.dumps(data)).text)
			
		finally:
			self.updating = False
	
	def act(self, action, env_name):
		# Whenever act gets called, increment update amount by one
		# TODO
		# Add separate metric for number of env calls (not just step based)
		self.update_amt += 1
		
		# Begin thread to send of batch of data
		if(self.updating == False):
			self.updating = True
			Thread(target=self.update_aiq).start()
		
		#Update information based on results of action
		self.observation, self.reward_step, self.done, self.info = self.env.step(action)
		self.reward_total += self.reward_step
		
		if self.log and self.done:
			self.results.append(self.reward_total)
			if len(self.results) == 20:
				self.log = False
				self.util_submit()
		
	def util_submit(self):
		avg_data = sum(self.results) / float(len(self.results))
		try:
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : avg_data,
				"test_name" : 'CartPole-v0_test'
			}
			# TODO 
			# Make verbose option
			data = requests.post(url, data=json.dumps(data)).text
		except:
			print("Failed to get data")
		finally:
			return data
		
	def submit(self):
		self.log = True
		self.results = []
		print("Logging next 20 simulations")
		
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
		try:
			import gym
		except:
			print("Failed to import gym, make sure you have OpenAI gym installed!")
			
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
		
class RPM(AIQ):
		
	def __init__(self):
		super().__init__()
		
	def get_train(self, amt):
		if amt > 750:
			print("Cannot request more than 750 examples")
			return None
			
		data = None
		try:
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : amt,
				"test_name" : '3_RPM_gen_train'
			}
			# TODO 
			# Make verbose option
			data = requests.post(url, data=json.dumps(data)).text
		except:
			print("Failed to get data")
		finally:
			return data
			
	def get_test(self):
		data = None
		try:
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : 10,
				"test_name" : '3_RPM_gen_test'
			}
			# TODO 
			# Make verbose option
			data = requests.post(url, data=json.dumps(data)).text
		except:
			print("Failed to get data")
		finally:
			self.data = data
			return data
			
	def submit(self, solution):
		try:
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : '"[[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]"',
				"test_name" : '3_RPM_evaluate'
			}
			# TODO 
			# Make verbose option
			data = requests.post(url, data=json.dumps(data)).text
		except:
			print("Failed to get data")
		finally:
			return data
		
	def connect(self):
		return super().connect()
		
# Make a ViZDoom class (to be tested on linux system, windows is meh for it)
#class ViZDoom(AIQ):
	
	

#


