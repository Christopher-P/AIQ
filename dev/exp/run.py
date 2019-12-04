import yaml
import sys
import os
from itertools import permutations, repeat
import traceback


# Go to where AIQ is installed
os.chdir('../../..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ
from DQN_M import DQN_Agent

#l1 = 'None'
#l2 = 'None'

# Runs agent on test 1, test2 and combined test
def run_agent(interface, name1, name2, k):
    #global l1

    print(name1, name2)

    try:
        interface.agent.clear()
        train_res = interface.join(name1, name2, k)
        #print(train_res.history)
        interface.fancy_logger(name1 + '=' + name2, 
                               train_res.history, 
                               file_name='dev/diversity/data/ensem', write='a')
        
        interface.agent.clear()
        train_res = interface.fit_to(name1,k)
        #print(train_res.history)
        interface.fancy_logger(name1, 
                               train_res.history, 
                               file_name='dev/diversity/data/ensem', write='a')

        interface.agent.clear()
        train_res = interface.fit_to(name2,k)
        #print(train_res.history)
        interface.fancy_logger(name2, 
                               train_res.history, 
                               file_name='dev/diversity/data/ensem', write='a')
        

    except Exception as e:
        print(e)
        traceback.print_exc()
        exit()
        return None


# generates a list of all pairwise combinations
def get_list(interface):
    names = []
    for ind,val in enumerate(interface.suites_added):
        #print(interface.suites_added[ind], interface.test_names[ind])        
        name = ''
        if interface.suites_added[ind] == 'ViZDoom':
            name = interface.suites_added[ind] + "_" + interface.test_names[ind]
        else:
            name = interface.test_names[ind]
        names.append(name)

    real_names = []

    for ind,val in enumerate(names):
        for ind2,val2 in enumerate(names):
            if ind2 < ind:
                continue
            real_names.append((val, val2))

    return real_names


def main():

    # Dummy credentials
    username = 'admin'
    password = 'password'

    # Setup AIQ system
    interface = AIQ(username, password)

    # Dont run Baseline Tests
    interface.bl = False 
    
    # Set our agent
    interface.agent = DQN_Agent()

    # Add the enves
    names = ["CartPole-v0", "CartPole-v1", "Acrobot-v1",
            "MountainCar-v0", "Roulette-v0","FrozenLake-v0" 
             "CliffWalking-v0","NChain-v0","FrozenLake8x8-v0", "Taxi-v2"]

    for name in names:
        interface.add(name)

    
    # For each test A, for each test B, train on a, train on b.
    for ind, A in interface.test_suite:
        for ind, B in interface.test_suite:
            name_A = A.header.env_name

    exit()


if __name__ == '__main__':
    main()

