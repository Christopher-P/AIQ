#!/usr/bin/python

import yaml
import sys
import os
from itertools import permutations, repeat
import traceback
import datetime

# Go to where AIQ is installed
os.chdir('../..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ
from DQN_M import DQN_Agent

#l1 = 'None'
#l2 = 'None'

# Runs agent on test 1, test2 and combined test
def run_agent(interface, name1, name2, k,p):
    #global l1
    #global l2
    '''
    if l1 != None:
        if l1 == name1 and l2 == name2:
            l1 = None            
            return None
        else:
            return None
    '''
    print(name1, name2)

    try:
        interface.agent.clear()
        train_res = interface.join(name1, name2, k)
        #print(train_res.history)
        interface.fancy_logger(name1 + '=' + name2, p,
                               train_res.history, 
                               file_name='dev/diversity/data-re/recal', write='a')
        
        interface.agent.clear()
        train_res = interface.fit_to(name1,k)
        #print(train_res.history)
        interface.fancy_logger(name1, p,
                               train_res.history,
                               file_name='dev/diversity/data-re/recal', write='a')

        interface.agent.clear()
        train_res = interface.fit_to(name2,k)
        #print(train_res.history)
        interface.fancy_logger(name2, p,
                               train_res.history, 
                               file_name='dev/diversity/data-re/recal', write='a')
        

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


def main(pos):

    #Import username and password
    #credentials = yaml.safe_load(open("credentials.yml"))

    # Dummy credentials
    username = 'admin'
    password = 'password'

    # Single Call
    interface = AIQ(username, password)

    # Dont run Baseline Tests
    interface.bl = False 
    
    # Set our agent
    interface.agent = DQN_Agent()

    # Add all envs
    # If ignore words found in env_name, dont add!
    ignore = ['Deterministic', 'ram', 'NoFrameskip']
    only_dim_in = 1
    only_dim_out = 1
    interface.add_all_tests(ignore, only_dim_in, only_dim_out)

    for ind,val in enumerate(interface.suites_added):
        print(interface.suites_added[ind], interface.test_names[ind])

    # Train/fit/log OOTB-agents
    names = get_list(interface)

    # Maximize effeciency
    
    #names = [('CartPole-v0', 'FrozenLake8x8-v0')]

    ## 13 * 55 
    val = names[pos]

    name1 = val[0]
    name2 = val[1]
    p = -1
    k = 100

    interface.agent.clear()
    train_res = interface.fit_to(name1,k)
    interface.fancy_logger(name1, p,
                           train_res.history,
                           file_name='dev/diversity/data/recal-' + str(name1), write='a')

    interface.agent.clear()
    train_res = interface.fit_to(name2,k)
    interface.fancy_logger(name2, p,
                           train_res.history, 
                           file_name='dev/diversity/data/recal-' + str(name2), write='a')

    for p in range(0,11)
        interface.agent.clear()
        train_res = interface.join(name1, name2, k, p/10.0)
        interface.fancy_logger(name1 + '=' + name2, p/10.0,
                               train_res.history, 
                               file_name='dev/diversity/data/recal-'+ 
                               str(name1) + '-' + str(name2), write='a')

if __name__ == '__main__':
    ## Parse args here
    pos = int(sys.argv[1])
    main(pos)
