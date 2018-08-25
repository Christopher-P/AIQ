import yaml

from test_suite import CartPole
from test_suite import RPM

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():

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
    for iter in range(10):
    
        #reset before each iteration
        AIQ_cart.reset()
        
        for ___ in range(200):
            AIQ_cart.render()
            AIQ_cart.act(AIQ_cart.env.action_space.sample()) # take a random action
            if AIQ_cart.done:
                break
        
        print(iter + 1, ": score = ", AIQ_cart.reward_total)
        
    #***** Begin RPM Example **********#
    
    AIQ_RPM = RPM()
    AIQ_RPM.username = credentials['username']
    AIQ_RPM.password = credentials['password']
    
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
    data = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    print(AIQ_RPM.submit(data))
    
    
    
if __name__ == '__main__':
    main()
    