import yaml
import time

from test_suite.MSPackman import MSPackMan
from test_suite.CartPole import CartPole
from test_suite.RPM import RPM

from test_suite.benchmark import Benchmark

from test_suite.gen import gen

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():
    #***** Begin RPM Example **********#
    username = credentials['username']
    password = credentials['password']
    AIQ_RPM = gen(username, password)
    
    #Check login data
    if not AIQ_RPM.connect():
        print("Invalid login Credentials")
        exit()
    
    # Request data from RPM generator (max 750)
    results_train = AIQ_RPM.get_train([750, 4])
    print(results_train)
    
    # Request data that needs a solution
    results_test = AIQ_RPM.get_test(4)
    print(results_test)
    
    #Submit a solution
    data = '"[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]"'
    print(AIQ_RPM.submit(data))
    
    exit()


    AIQ_Pack = MSPackMan()
    
    # Pass in our login info
    AIQ_Pack.username = credentials['username']
    AIQ_Pack.password = credentials['password']
    
    # For debugging
    # print(AIQ_Pack.username, AIQ_Pack.password)
    
    #Check login data
    if not AIQ_Pack.connect():
        print("Invalid login Credentials")
        exit()

    # Run 10 times
    for iter in range(1):
    
        #reset before each iteration
        AIQ_Pack.reset()
        
        for ___ in range(200):
            AIQ_Pack.render()
            AIQ_Pack.act(AIQ_Pack.env.action_space.sample()) # take a random action
            if AIQ_Pack.done:
                break
        
        print(iter + 1, ": score = ", AIQ_Pack.reward_total)

    #***** Begin RPM Example **********#
    username = credentials['username']
    password = credentials['password']
    AIQ_RPM = RPM(username, password)
    
    #Check login data
    if not AIQ_RPM.connect():
        print("Invalid login Credentials")
        exit()
    
    # Request data from RPM generator (max 750)
    results_train = AIQ_RPM.get_train(750)
    print(results_train)
    
    # Request data that needs a solution
    results_test = AIQ_RPM.get_test()
    print(results_test)
    
    #Submit a solution
    data = '"[[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]"'
    print(AIQ_RPM.submit(data))
    
    exit()

    bench = Benchmark(['RPM'])
    bench.begin()


    # Declare our AIQ object
    AIQ_cart = CartPole()
    
    # Pass in our login info
    AIQ_cart.username = credentials['username']
    AIQ_cart.password = credentials['password']
    
    # For debugging
    #print(AIQ_cart.username, AIQ_cart.password)
    
    #Check login data
    if not AIQ_cart.connect():
        print("Invalid login Credentials")
        exit()

    # Run 10 times
    for iter in range(1):
    
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
    