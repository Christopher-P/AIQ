import yaml
import sys
import os

# Go to where AIQ is installed
os.chdir('../..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ
from DQN import DQN_Agent

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

    # Add all envs
    interface.add('OpenAIGym', {'env_name':'CartPole-v0'})

    
    # Set our agent
    for i in range(11,12):
        interface.agent = None
        interface.agent = DQN_Agent(i * 10)
        train_res = interface.fit_to('CartPole-v0')
        print(train_res)
        interface.fancy_logger('CartPole-v0 ' + str(i * 10),
                               train_res.history, 
                               file_name='dev/diversity/data/handicapping', write='a')

    exit()



if __name__ == '__main__':
    main()

#37655
#16504655
