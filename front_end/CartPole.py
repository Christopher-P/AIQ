import _pickle as cPickle
import yaml

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():
	#Un Pickle our environment
	pickle_in = open("dict.pickle","rb")
	AIQ = cPickle.load(pickle_in)

	#Setup AIQ login data
	AIQ.username = credentials.username
	AIQ.password = credentials.password
	
	#Check login data
	AIQ.connect()

	
	env2.reset()
	for _ in range(1000):
		env2.render()
		env2.step(env2.action_space.sample()) # take a random action
		
		
if __name__ == '__main__':
	main()