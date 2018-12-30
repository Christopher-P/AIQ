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

        self.agent = 1
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
        if self.bl:
            bl1 = bl_mnist()
            self.results['MNIST'] = bl1.run_bl()
            bl2 = bl_cifar10()
            self.results['CIFAR10'] = bl2.run_bl()

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

    # Helper functions to cleanup code
    def rl_test(self, test):
        score = 0.0
        trials = 10
        for i in range(trials):
            test.reset()
            while test.done == False:
                #TODO: Make general accros all tests (proof of concept atm)
                #TODO: This is here because creating an agent to handle many different inputs is hard
                if test.get_header().env_name == "ViZDoom_Basic":
                    test.act(test.random_action())
                else:
                    test.act(test.action_space.sample()) # take a random action
            score += test.reward_total

            f_score = self.norm(float(score/trials), 
                                test.header.env_min_score, 
                                test.header.env_max_score)

            if f_score > 1.0:
                return 1.0
            else:
                return f_score

    def ds_test(self, test):
        preds = []
        for i in test.get_test():
            preds.append([0,1,2,3])

        f_score = self.norm(test.evaluate(preds), 
                            test.header.env_min_score, 
                            test.header.env_max_score)
        if f_score > 1.0:
            return 1.0
        else:
            return f_score

    def norm(self, score, min_s, max_s):
        return (score - min_s) / (max_s - min_s)

