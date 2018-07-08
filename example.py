import yaml

from AIQ import CartPole

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():
	#Un Pickle our environment
	
	AIQ_cart = CartPole()
	AIQ_cart.username = credentials['username']
	AIQ_cart.password = credentials['password']
	
	print(AIQ_cart.username, AIQ_cart.password)
	
	#Check login data
	if not AIQ_cart.connect():
		print("Invalid login Credentials")

	#start = datetime.datetime.now()
	#First trial

	for iter in range(10):
	
		#reset before each iteration
		AIQ_cart.reset()
		
		for ___ in range(200):
			AIQ_cart.render()
			AIQ_cart.act(AIQ_cart.env.action_space.sample()) # take a random action
			if AIQ_cart.done:
				break
		
		print(iter + 1, ": score = ", AIQ_cart.reward_total)
		
if __name__ == '__main__':
	main()
	