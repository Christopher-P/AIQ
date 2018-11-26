from .backend import backend_handler_new
from .test_suite.bl_mnist import bl_mnist
from .test_suite.bl_cifar10 import bl_cifar10
import importlib

class AIQ():

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.backend = backend_handler_new(self.username, self.password)

        self.agent = 1
        self.test_suite = []
        self.results = {}

    # Check connection
    def connect(self):
        return self.backend.connect()

    # Add a test to the test suite
    def add(self, env_name):
        # https://stackoverflow.com/questions/547829/
        try:
            mod = __import__('AIQ.test_suite', fromlist=[env_name])
            klass = getattr(mod, env_name)
            kless = getattr(klass, env_name)
            inst = kless()
            self.test_suite.append(inst)
            print("{} was added to the suite!".format(env_name))
        except:
            print("{} was not found in the test_suite directory!".format(env_name))



    # Evaluate test suite and given agent
    def evaluate(self):
        if self.agent == None:
            print("No agent defiend")
        if len(self.test_suite) == 0:
            print("No tests defined")

        # Run BL for speed testing
        
        bl1 = bl_mnist()
        self.results['MNIST'] = bl1.run_bl()
        bl2 = bl_cifar10()
        self.results['CIFAR10'] = bl2.run_bl()
        print(self.results)
        
        for test in self.test_suite:
            # Seperate tests by RL or DS
            if test.rl == True:
                self.results[test.name] = self.rl_test(test)
            else:
                self.results[test.name] = self.ds_test(test)
                
    # Send results to AIQ website
    def submit(self):
        return self.backend.submit(self.results)
        

    # Helper functions to cleanup code
    def rl_test(self, test):
        score = 0.0
        trials = 10
        for i in range(trials):
            test.reset()
            while test.done == False:
                # agent will look like
                '''
                action = self.agent.act(header, test.obs)
                self.test(action)
                '''
                test.act(test.action_space.sample()) # take a random action
            score += test.reward_total
        return float(score/trials)

    def ds_test(self, test):
        print("TODO")


