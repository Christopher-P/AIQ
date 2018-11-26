### Ideal functionality
import yaml
import time
import sys
sys.path.insert(0, "/home/chris/Desktop/github/AIQ")

### Import AIQ package
from AIQ.AIQ import AIQ
# from AIQ import agent_class

def main():
    #Import username and password
    credentials = yaml.safe_load(open("credentials.yml"))

    username = credentials['username']
    password = credentials['password']

    # Single Call
    interface = AIQ(username, password)
    
    # Check login data
    if not interface.connect():
        print("Invalid login Credentials")
        exit()

    # Load test suite
    interface.add('CartPole')
    interface.add('RPM')

    # What if it is not in set?
    interface.add('none_test')

    # Set our agent
    # Overloads agent class
    interface.agent = agent_class()

    interface.evaluate()
    
    print(interface.results)

    interface.submit()
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
    



 


if __name__ == '__main__':
    main()
