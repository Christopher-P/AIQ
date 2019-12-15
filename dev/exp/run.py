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

    # Add all tests we need
    for name in names:
        interface.add('OpenAIGym', {'env_name':name})

    # Used for starting and stopping exp mid way
    save_point = None
    #save_point = ['FrozenLake8x8-v0','CliffWalking-v0']

    # For each test A, for each test B, train on a, train on b.
    for ind, A in enumerate(interface.test_suite):
         # Get env names
        name_A = A.header.env_name

        # Train on initial problem
        history_A = interface.fit_to(name_A)

        # Save model (so we dont need to retrain)
        interface.agent.model.save('A_model.h5')

        for ind, B in enumerate(interface.test_suite):
               
            # Get env names
            name_B = B.header.env_name
            print(name_A, name_B)

            # Used for if the system crashes or we need to interupt data gathering
            if save_point != None:
                if name_A != save_point[0] or name_B != save_point[1]:
                    continue
                else:
                    save_point = None

            # Reset and load base problem
            interface.agent.clear()
            interface.agent.model = load_model('A_model.h5')

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
            record('Ratio.csv', name_A, name_B, Ratio)

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

