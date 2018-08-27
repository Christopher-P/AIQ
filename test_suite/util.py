import json
import requests
from threading import Thread, Lock

# Define common header for all envs to use
class Header():

    def __init__(self, name, input_dim, output_dim, definition):
        self.name = name
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.definition = definition
    
    def get_name(self):
        return self.name
        
    def get_input_dim(self):
        return self.input_dim
        
    def get_output_dim(self):
        return self.output_dim
    
    def get_definition(self):
        return self.definition


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