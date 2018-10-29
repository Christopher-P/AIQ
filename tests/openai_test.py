import sys
sys.path.insert(0, "/home/chris/Desktop/github/AIQ")

import yaml
import time

from AIQ.test_suite.openai import OpenAI

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():

    # Declare our AIQ object
    AIQ_cart = OpenAI("CartPole-v0")
    
    # Pass in our login info
    AIQ_cart.username = credentials['username']
    AIQ_cart.password = credentials['password']
    
    #Check login data

    if not AIQ_cart.connect():
        print("Invalid login Credentials")
        exit()

    #Load Action Space
    actions = AIQ_cart.input_dim

    # Run 10 times
    for iter in range(1):
    
        #reset before each iteration
        AIQ_cart.reset()
        
        for ___ in range(200):
            AIQ_cart.render()
            AIQ_cart.act(AIQ_cart.input_dim.sample()) # take a random action
            if AIQ_cart.done:
                break
        
        print(iter + 1, ": score = ", AIQ_cart.reward_total)
        
if __name__ == '__main__':
    main()
    
