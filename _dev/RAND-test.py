import yaml
import sys
import os

# Go to where AIQ is installed
os.chdir('..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ
from RAND import RAND_Agent

def main():

    #Import username and password
    credentials = yaml.safe_load(open("credentials.yml"))

    # Dummy credentials
    username = 'admin'
    password = 'password'

    # Single Call
    interface = AIQ(username, password)

    # Dont run Baseline Tests
    interface.bl = False 
    
    # Set our agent
    interface.agent = RAND_Agent()

    interface.add('OpenAIGym', {'env_name':'Taxi-v2'})
    interface.fit_to('Taxi-v2')
    print(interface.test_to('Taxi-v2', 20))
    exit()

    # Add all envs
    # If ignore words found in env_name, dont add!
    ignore = ['Deterministic', 'ram', 'NoFrameskip']
    interface.add_all_tests(ignore)

    for ind,val in enumerate(interface.suites_added):
        print(interface.suites_added[ind], interface.test_names[ind])

    last = None

    # Train/fit/log OOTB-agents
    for ind,val in enumerate(interface.suites_added):
        if last is not None:
            if interface.test_names[ind] == last:
                last = None
            else:
                continue

        print(interface.suites_added[ind], interface.test_names[ind])        
        name = ''

        if interface.suites_added[ind] == 'ViZDoom':
            name = interface.suites_added[ind] + "_" + interface.test_names[ind]
        else:
            name = interface.test_names[ind]

        interface.fit_to(name)
        results = interface.test_to(name, 20)
        interface.fancy_logger(interface.suites_added[ind], 
                               interface.test_names[ind], 
                               results, 
                               file_name='dev/data/RAND-Data', write='a')

    exit()


if __name__ == '__main__':
    main()
