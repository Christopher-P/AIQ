import yaml
import datetime

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

# Example of yaml file
# username:
#    Joe_Smith
#    
# password:
#    password123

def main():
	#Un Pickle our environment
	pickle_in = open("../back_end/CartPole-v0.pickle","rb")
	AIQ = cPickle.load(pickle_in)
	
	AIQ.init_()

	#Setup AIQ login data
	AIQ.username = credentials['username']
	AIQ.password = credentials['password']
	
	print(AIQ.username, AIQ.password)
	
	#Check login data
	#Connect needs implementation
	#AIQ.connect()

	start = datetime.datetime.now()
	#First trial
	AIQ.reset()
	for ___ in range(100):
		AIQ.render()
		AIQ.act(AIQ.action_space.sample()) # take a random action
	
	stop = datetime.datetime.now()
	print(stop - start)
		
		
if __name__ == '__main__':
	main()