import sys
import os
import csv

# Supress warnings
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from keras.models import load_model

# Go to where AIQ is installed
os.chdir('../..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ
from DQN_M import DQN_Agent


scales = {'CartPole-v0':(15.0, 261.0), 
          'CartPole-v1':(15.0, 265.0),
          'Acrobot-v1':(-699.0, -615.0), 
          'MountainCar-v0':(-399.0, 200.0), 
          'Roulette-v0':(-71.0, 144.0), 
          'FrozenLake-v0':(0.0, 1.0), 
          'CliffWalking-v0':(-26058.0, -143.0), 
          'NChain-v0':(1318.0, 1782.0), 
          'FrozenLake8x8-v0':(0.0, 1.0), 
          'Taxi-v2':(-1164.0, -162.0)}

# includes the scaled 90%
# bool indicates if average is needed
max_vals = {'CartPole-v0'   :[180.0, False], 
          'CartPole-v1'     :[450.0, False],
          'Acrobot-v1'      :[-110.0, False],
          'MountainCar-v0'  :[180.0, False],
          'Roulette-v0'     :[0.0, True],     # avg 
          'FrozenLake-v0'   :[0.9, True],    # avg 
          'CliffWalking-v0' :[-170.0, False], 
          'NChain-v0'       :[900.0, False], 
          'FrozenLake8x8-v0':[0.9, True],     # avg
          'Taxi-v2'         :[-180.0, False]}

# Uniform function to save experimental data
def record(filename, nameA, values):
    with open('dev/complexity/data/' + filename, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow((nameA, values))
    return None


def main():

    # If avg, how many to avg?
    samples = 50

    global max_vals

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

    # Add all tests we need
    for name in names:
        interface.add('OpenAIGym', {'env_name':name})

    for ind, A in enumerate(interface.test_suite):
           
        # Get env names
        name_A = A.header.env_name
        print(name_A)

        # Reset and load base problem
        interface.agent.clear()

        # Train agent until score is reached
        done = False
        A_r = []

        print(name_A, max_vals[name_A][0])
        history_A = interface.fit_to(name_A, max_vals[name_A][0])

        ind_m = -1
        
        # If no avg is needed
        if not max_vals[name_A][1]:
            for ind, val in enumerate(history_A.history['episode_reward']):
                if val > max_vals[name_A][0]:
                    ind_m = ind
                    break
        # If avg is needed        
        else:
            roll = [-9999999999]*samples
            c = 0
            for ind, val in enumerate(history_A.history['episode_reward']):
                if sum(roll)/len(roll) > max_vals[name_A][0]:
                    ind_m = ind
                    break
                roll[c] = val
                c += 1
                if c >= samples:
                    c = 0
        record('Epochs.csv', name_A, ind_m)
       
        # Record all data
        # Just so if we change something we dont need to rerun everything
        record('RAW.csv', name_A, history_A.history)

    exit()


if __name__ == '__main__':
    main()

