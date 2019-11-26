import yaml
import sys
import os

### Comment out when running actual docker
credentials = yaml.safe_load(open("credentials.yml"))
os.chdir('..')
sys.path.insert(0, os.getcwd())

### Import AIQ package
from AIQ.AIQ import AIQ

### Import complexity agent
from AIQ.agents.complexity_agent import C_Agent

def main():

    #Import username and password
    global credentials

    username = credentials['username']
    password = credentials['password']

    # Single Call
    interface = AIQ(username, password)

    # Dont run Baseline Tests
    interface.bl = False 
    
    ### Setup Complexity agent
    interface.agent = C_Agent()

    ### Add one env to test system
    #interface.add('OpenAIGym', {'env_name':'CartPole-v0'})

    #r = interface.backend.send_complexity(2, 2, 2, 2)
    #print(r.text)
    #exit()

    ### Add all envs to test suite
    ## If ignore words found in env_name, dont add!
    ignore = ['Deterministic', 'ram', 'NoFrameskip']
    interface.add_all_tests(ignore)

    for inst in interface.test_suite:
        ## Set new test env
        print(type(inst))
        interface.agent.reset(inst)
        print(inst)

        ## Train agent, returns epochs and trainable params and non-trainable params
        e, tp, ntp = interface.agent.train()
        print(e,tp,ntp)

        ## Get test name
        r = interface.backend.send_complexity(inst.header.env_name, e, tp, ntp)
        print(r)

if __name__ == '__main__':
    main()
