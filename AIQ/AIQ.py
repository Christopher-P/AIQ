from .backend import backend_handler
from .test_suite.bl_mnist import bl_mnist
from .test_suite.bl_cifar10 import bl_cifar10
import importlib

class AIQ():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bl       = True
        self.backend  = backend_handler(self.username, self.password)

        self.agent = None
        self.test_suite = []
        self.results = {}

    # Check connection
    def connect(self):
        return self.backend.connect()

    # Add a test to the test suite
    def add(self, env_name, params=None):
        # https://stackoverflow.com/questions/547829/
        try:
            mod = __import__('AIQ.test_suite', fromlist=[env_name])
            klass = getattr(mod, env_name)
            kless = getattr(klass, env_name)
            if params == None:
                inst = kless()
            else:
                inst = kless(params)
            self.test_suite.append(inst)
            if params is not None and 'env_name' in params:
                print("{}: {} was added to the suite!".format(env_name, params['env_name']))
            else:
                print("{} was added to the suite!".format(env_name))
        except:
            if params is not None and 'env_name' in params:
                print("{}: {} was not found in the test_suite directory!".format(env_name, params['env_name']))
            else:
                print("{}  was not found in the test_suite directory!".format(env_name))
                



    # Evaluate test suite and given agent
    def evaluate(self):
        if self.agent == None:
            print("No agent defiend")
        if len(self.test_suite) == 0:
            print("No tests defined")

        # Run BL for speed testing
        if self.bl:
            bl1 = bl_mnist()
            self.results['MNIST'] = bl1.run_bl()
            bl2 = bl_cifar10()
            self.results['CIFAR10'] = bl2.run_bl()

        # Run test suite using defined agent
        for test in self.test_suite:
            # Seperate tests by RL or DS
            if test.get_header().rl == True:
                self.results[test.get_header().env_name] = self.rl_test(test)
            else:
                self.results[test.get_header().env_name] = self.ds_test(test)

        # For now simple average computed client side
        # TODO Move to server side
        # TODO Use weighted average!
        AIQ = 0.0
        for key, val in self.results.items():
            AIQ += val
        AIQ = AIQ / len(self.results)
        self.results['AIQ'] = AIQ
                
    # Send results to AIQ website
    def submit(self):
        return self.backend.submit(self.results)

    # Used to train an agent on a subset of the test suite
    #TODO: Make work for 1 test
    #TODO: Make work for n tests
    def fit_to(self, test_name):
        # Search test suite for test
        inst = None
        for test in self.test_suite:
            if test_name == test.header.env_name:
                inst = test

        print(inst)

    # Helper functions to cleanup code
    def rl_test(self, test):
        score = 0.0
        trials = 10
        for i in range(trials):
            test.reset()
            while test.done == False:
                observation = test.observation
                action = self.agent.act(test.header, observation)
                test.act(action)

            score += test.reward_total

            f_score = self.norm(float(score/trials), 
                                test.header.env_min_score, 
                                test.header.env_max_score)

            # catchall incase score doesnt get normalized
            if f_score > 1.0:
                return 1.0
            else:
                return f_score

    # Called for dataset tests
    def ds_test(self, test):
        test_data = test.get_test()
        predictions = self.agent.predict(test.header, test_data)
        score = test.evaluate(predictions)

        f_score = self.norm(score, 
                            test.header.env_min_score, 
                            test.header.env_max_score)

        # catchall incase score doesnt get normalized
        if f_score > 1.0:
            return 1.0
        else:
            return f_score

    # Score normalization
    def norm(self, score, min_s, max_s):
        return (score - min_s) / (max_s - min_s)

