

class ClassName(AIQ):
    
    def __init__(self):
        super().__init__()
        try:
            # Locate external files / environments here
        except:
            # print("Unable to find environment!")
         
        # Define the environment
        #self.env = 
        #self.action_space = self.env.action_space
        self.header = Header('env', 0, 0, 'env desc')
    
    def get_header(self):
        return self.header
        
    def connect(self):
        return super().connect()
        
    # If env object has rendering capabilities
    def render(self):
        #self.env.render()
    
    def act(self, action):
        #return super().act(action, 'CartPole-v0')
        
    def reset(self):
        #super().reset()
        #self.env.reset()
        


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
