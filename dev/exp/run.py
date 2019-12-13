import yaml
import sys
import os
from itertools import permutations, repeat
import traceback

import csv


# Go to where AIQ is installed
os.chdir('../..')
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

def record(filename, nameA, nameB, values, values2=None):
    with open('dev/exp/data/' + filename, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        if values2 == None:
            spamwriter.writerow((nameA, nameB, values))
        else:
            spamwriter.writerow((nameA, nameB, values, values2))
    return None

# Takes a list of values, returns the area under the curve
def AuC(data):

    Area = 0.0

    for ind,val in enumerate(data):

        # Dont do last value
        if ind >= len(data) - 1:
            continue
        
        # Calculate box area
        h = min(data[ind], data[ind+1])
        w = 1       # Assume constant width for now

        box_area = h*w

        # Calculate triangle area
        h = max(data[ind], data[ind+1]) - min(data[ind], data[ind+1])
        w = 1       # Assume constant width for now
        
        triangle_area = h*w/2.0

        # Add box and triangle to area
        Area += box_area + triangle_area

    return Area
        

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
            "MountainCar-v0", "Roulette-v0","FrozenLake-v0",
             "CliffWalking-v0","NChain-v0","FrozenLake8x8-v0", "Taxi-v2"]

    # TODO:
    # We need to measure 5 metrics:

    # Jumpstart: The initial performance of an agent in a target task may 
    # be improved by transfer from a source task.

    # Asymptotic Performance: The final learned performance of an 
    # agent in the target task may be improved via transfer.

    # Total Reward: The total reward accumulated by an agent (i.e., the area under the learning
    # curve) may be improved if it uses transfer, compared to learning without transfer

    # Transfer Ratio: The ratio of the total reward accumulated by the transfer 
    # learner and the total reward accumulated by the non-transfer learner.

    # Time to Threshold: The learning time needed by the agent to achieve a pre-specified
    # performance level may be reduced via knowledge transfer.
    #interface.add_all_tests()

    for name in names:
        interface.add('OpenAIGym', {'env_name':name})

    save_point = None
    # save_point = ['name_A','name_B']

    # For each test A, for each test B, train on a, train on b.
    for ind, A in enumerate(interface.test_suite):
        for ind, B in enumerate(interface.test_suite):
               
            # Get env names
            name_A = A.header.env_name
            name_B = B.header.env_name
            print(name_A, name_B)

            # Used for if the system crashes or we need to interupt data gathering
            if save_point != None:
                if name_A != save_point[0] or name_B != save_point[1]:
                    continue
                else:
                    save_point = None

            # Train on initial problem
            history_A = interface.fit_to(name_A)

            # Transfer onto second problem
            history_B = interface.fit_to(name_B)

            # Get episode rewards
            A_r = history_A.history['episode_reward']
            B_r = history_B.history['episode_reward']
 
            # Record JumpStart
            # agent_B_init_score - agent_A_init_score
            JumpStart = B_r[0] - A_r[0]
            record('JumpStart.csv', name_A, name_B, JumpStart)

            # Record Asymptotic Performance
            # agent_B_final_score - agent_A_final_score
            samples_AP = 5                  # Number of samples at end
            Asymptotic = (sum(B_r[-samples_AP:])/samples_AP) - (sum(A_r[-samples_AP:])/samples_AP)
            record('Asymptotic.csv', name_A, name_B, Asymptotic)

            # Record Total Reward
            # Makes more sense to do average (since a lot are time dependent)
            # sum(A_reward) - sum(B_reward)
            try:
                Reward = (sum(B_r) / len(B_r)) - (sum(A_r) / len(A_r))
            except:
                Reward = -999999
            record('Reward.csv', name_A, name_B, Reward)

            # Record Transfer Ratio
            # (AuC_B - AuC_A) / AuC_A
            try:
                Ratio = (AuC(B_r) - AuC(A_r)) / AuC(A_r)
            except:
                Ratio = -999999
            record('Ratio.csv', name_A, name_B, Reward)

            # Record Time to Threshold
            # Min(time_A > 0.95) - Min(time_B > 0.95)
            # TODO: Ignoring for now, need to normalize openaigym values
            #        Can be done after with raw data.


            # Record all data
            # Just so if we change something we dont need to rerun everything
            record('RAW.csv', name_A, name_B, history_A.history, history_B.history)


    exit()


if __name__ == '__main__':
    main()

