import yaml
import sys
import os

### Comment out when running actual docker
credentials = yaml.safe_load(open("credentials.yml"))
os.chdir('..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ

### Import random agent
from AIQ.agents.random_agent import R_Agent

def main():

    #Import username and password
    global credentials

    username = credentials['username']
    password = credentials['password']

    # Single Call
    interface = AIQ(username, password)

    # Dont run Baseline Tests
    interface.bl = False 
    
    # Check login credentials
    if not interface.connect():
        print("Invalid login Credentials")
        print(interface.backend.response.text)
    #    exit()

    # Load server-side tests
    # Pass in the backend handler
    #TODO:  Maybe think of better way to send backend to test
    #       Currently being sent this way so we dont store 
    #       user/pass in more than one spot
    #TODO: Fix RPM (broke in backend update)
    #interface.add('RPM', interface.backend)

    test_name = "Not_RPM"
    epochs = -1
    params = -1

    r = interface.backend.send_complexity(test_name, epochs, params)

    #print(r.text)
    
    # Load test suite
    #interface.add('OpenAIGym', {'env_name':'CartPole-v0'})
    #interface.add('OpenAIGym', {'env_name':'Acrobot-v1'})
    #interface.add('ALE',       {'env_name':'MsPacman-v0'})
    #interface.add('AI2')
    
    # Sample for loading params into a test
    #params = {}
    #params['config'] = "AIQ/test_suite/vizdoom_scenarios/basic.cfg"
    #params['env_name'] = "basic"
    #interface.add('ViZDoom', params=params)
    
    # Tests not in suite will display [test_name] was not found.
    #interface.add('none_test')
    
    # Set our agent
    #interface.agent = R_Agent()

    # Run agent on test suite
    #interface.evaluate()
    
    # Print results (dictionary) from evaluation
    #print(interface.results)

    # Submit and print server feedback
    #print(interface.submit())


if __name__ == '__main__':
    main()
