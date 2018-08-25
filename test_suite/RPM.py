import json
import requests
from threading import Thread, Lock

from .util import AIQ

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
			print(url, data=json.dumps(data))
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
		

'''        
class RPM_exe(AIQ):

	def __init__(self):		
		from subprocess import Popen, PIPE
		self.p = Popen(['AIQ_Front.exe'], shell=True, stdout=PIPE, stdin=PIPE)
		
	def get_train(self, amt):
		value = str(amt) + '\n'
		value = bytes(value, 'UTF-8')  # Needed in Python 3.
		self.p.stdin.write(value)
		self.p.stdin.flush()
		result = self.p.stdout.readline().strip()
		print(result)
			
	def get_test(self):
		value = bytes(amt, 'UTF-8')  # Needed in Python 3.
		p.stdin.write(value)
		p.stdin.flush()
		result = p.stdout.readline().strip()
		print(result)
			
	def submit(self, solution):
		value = bytes(amt, 'UTF-8')  # Needed in Python 3.
		p.stdin.write(value)
		p.stdin.flush()
		result = p.stdout.readline().strip()
		print(result)
		
	def connect(self):
		return super().connect()
        
'''