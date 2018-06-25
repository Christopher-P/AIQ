import json
import requests
from threading import Thread, Lock

class AIQ():

	def __init__(self, env):
		self.env = env
		self.action_space = env.action_space
		
	def getInfo(self):
		return self
		
	def init_(self):
		self.observation = None
		self.reward = None
		self.done = None
		self.info = None
		self.password = None
		self.username = None
		self.updating = False

		self.mutex = Lock()
		self.update_amt = 0
		print("done")
		
	def reset(self):
		self.env.reset()
		
	def update(self):
		self.mutex.acquire()
		try:
			if(self.update_amt == 0):
				return None
				
			url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
			data = {
				"username"  : self.username,
				"password"  : self.password,
				"data"      : 1,
				"test_name" : "CartPole-v0"
			}
			print(requests.post(url, data=json.dumps(data)), self.update_amt)
		finally:
			self.updating = False
			self.update_amt = 0
			self.mutex.release()
	
	def act(self, action):
		self.update_amt = 1
		if(self.updating == False):
			self.updating = True
			Thread(target=self.update).start()
		
		self.observation, self.reward, self.done, self.info = self.env.step(action)
	
	def render(self):
		self.env.render()
		
	def connect(self):
		# TODO
		return None
		
	def get_env(self):
		return self.env