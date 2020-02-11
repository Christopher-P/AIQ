### Noise added to classificaiton data with known disimilarity
### Will verify Similarity method with this first method

# System utils
import os 
import sys

# Goto AIQ
os.chdir('../..')
sys.path.insert(0, os.getcwd())
from AIQ.AIQ import AIQ
from DQN_M import DQN_AGENT

# Import similarity util
from sim_util import Similarity

## Experiment parameters
seed = 123
proportion = 0.5
trials = 10
# p = 0.0 --> all B, p = 1.0 --> all A
## End parameters

def logger(Aname, Bname, A, B, AB, S, seed, trials, proportion):
    return None

def main()
    global seed
    global proportion
    global trials

    ### Create AIQ interface
    interface = AIQ("","")

    ### Add classification test
    names = {'CIFAR10':{'env_name':'CIFAR10'}}
    for i in names.keys()
        interface.add(i, names[i])

    ### Add modifcation of classification dataset


    ### Setup 
    sim_backend = Similarity(interface)

    ## Run experiment
    for testA in interface.tests:
        for testB in interface.tests:
            # Get test instances
            sim_backend.testA = testA
            sim_backend.testB = testB
            
            # Run it
            A,B,AB,S = sim_backend.run(seed=seed,trials=trials,p=proportion)
            # Log it
            log(testA_name, testB_name, A, B, AB, S, seed, trials, proportion)



if __name__ == "__main__":
    main()
