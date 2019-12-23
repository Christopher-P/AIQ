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

# Uniform function to save experimental data
def record(filename, nameA, k, values):
    with open('dev/handicapping/data/' + filename, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow((nameA, k, values))
    return None


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

    # Add all tests we need
    for name in names:
        interface.add('OpenAIGym', {'env_name':name})


    for counter in range(10):
        for ind, A in enumerate(interface.test_suite):
               
            # Get env names
            name_A = A.header.env_name
            print(name_A)

            # Reset and load base problem
            interface.agent.clear()

            history_A = interface.fit_to(name_A, counter * 10)

            record('Epochs.csv', name_A, counter * 10, ind_m)
           
            # Record all data
            # Just so if we change something we dont need to rerun everything
            record('RAW.csv', name_A, counter * 10, history_A.history)

    exit()


if __name__ == '__main__':
    main()

