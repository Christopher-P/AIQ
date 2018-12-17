import yaml
import sys

#TODO: Finalize package to remove relative imports
sys.path.insert(0, "/home/chris/Desktop/github/AIQ")

### Import AIQ package
from AIQ.AIQ import AIQ
#TODO: Finish implementation
# from AIQ.AIQ.agents import random_agent

def main():
    #Import username and password
    credentials = yaml.safe_load(open("credentials.yml"))

    username = credentials['username']
    password = credentials['password']

    # Single Call
    interface = AIQ(username, password)

    # Dont run Baseline Tests
    interface.bl = False
    
    # Check login data
    if not interface.connect():
        print("Invalid login Credentials")
        exit()
    
    # Load test suite
    interface.add('MSPackman')
    interface.add('CartPole')
    interface.add('AI2')

    # Sample for loading params into a test
    # TODO Change to relative import!!
    params = {}
    params['config'] = "../AIQ/test_suite/vizdoom_scenarios/basic.cfg"
    params['subtest'] = "Basic"
    interface.add('ViZDoom', params=params)

    # Tests not in suite will display [test_name] was not found.
    interface.add('none_test')

    # Set our agent
    # Overloads agent class
    # TODO add this
    # interface.agent = random_agent()

    # Run agent on test suite
    interface.evaluate()
    
    # Print results (dictionary) from evaluation
    print(interface.results)

    # Submit and print server feedback
    print(interface.submit())


if __name__ == '__main__':
    main()
