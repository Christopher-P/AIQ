from .backend import backend_handler
from .test_suite.bl_mnist import bl_mnist
from .test_suite.bl_cifar10 import bl_cifar10
from .test_suite.util import tests

# Used for loading tests into test suite
import importlib

# Used for animations
import itertools
import threading
import time

# Used for logging results
import csv
import statistics 

from .test_suite.inst_wrapper import wrap

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
    def add(self, env_name, out, params=None):
        # https://stackoverflow.com/questions/547829/
        try:
            mod = __import__('AIQ.test_suite', fromlist=[env_name])
            klass = getattr(mod, env_name)
            kless = getattr(klass, env_name)
            inst = kless(params)

            if len(inst.get_header().output_dim) != out:
                raise Exception('Dis-allowed output dimension')

            self.test_suite.append(inst)
            if params is not None and 'env_name' in params:
                print("{}: {} was added to the suite!".format(env_name, params['env_name']))
            else:
                print("{} was added to the suite!".format(env_name))
            return True
        except:
            if params is not None and 'env_name' in params:
                print("{}: {} was not found in the test_suite directory!".format(env_name, params['env_name']))
            else:
                print("{}  was not found in the test_suite directory!".format(env_name))
            return False

    # Add all available test envs to the suite
    def add_all_tests(self, ignore, inp, out):
        # Class used to get the list of tests
        tests_class = tests()
        # Get test subsuites and env_names
        suites, test_names = tests_class.list_all()
        self.suites_added = []
        self.test_names   = []

        # Go through list and add each test
        for ind, val in enumerate(test_names):
            found = False
            for word in ignore:
                if word in test_names[ind]:
                    found = True
            if not found:
                if self.add(suites[ind],out, {'env_name':test_names[ind]}):
                    # All input dims are one dimensional, will change with img -> img problems
                    self.suites_added.append(suites[ind])
                    self.test_names.append(test_names[ind])

        return None

    # Used to merge tests utilzing a wrapper
    def join(self, name1, name2):
        # Search test suite for test
        inst1 = None
        for test in self.test_suite:
            if name1 == test.header.env_name:
                inst1 = test

        if inst1 == None:
            print('Cannot fit to: ' + name1)
            print(name1 + ' not found in active suite!')

        # Search test suite for test
        inst2 = None
        for test in self.test_suite:
            if name2 == test.header.env_name:
                inst2 = test

        if inst2 == None:
            print('Cannot fit to: ' + name2)
            print(name2 + ' not found in active suite!')

        print(inst1,inst2)
        wr = wrap(inst1, inst2)
        return self.agent.fit_to(wr)

    # Evaluate test suite and given agent
    def evaluate(self):
        # TODO: Do users need to define agent?
        if self.agent == None:
            print("No agent defiend")
        if len(self.test_suite) == 0:
            print("No tests defined")

        # Run BL for speed testing
        if self.bl:
            self.animation('Running Baselines', 'Baselines finished!')
            bl1 = bl_mnist()
            self.results['MNIST'] = bl1.run_bl()
            bl2 = bl_cifar10()
            self.results['CIFAR10'] = bl2.run_bl()
            self.stop_animation()

        # Run test suite using defined agent
        self.animation('Running test suite', 'Finished Test Suite')
        for test in self.test_suite:
            test_name = test.get_header().env_name

            # Seperate tests by RL or DS
            if test.get_header().rl == True:
                self.results[test_name] = self.rl_test(test)
            else:
                self.results[test_name] = self.ds_test(test)
            
        self.stop_animation()

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
    def fit_to(self, test_name):
        # Make sure agent exists
        if self.agent == None:
            print('ERROR: No agent defined')
            return None

        # Search test suite for test
        inst = None
        for test in self.test_suite:
            if test_name == test.header.env_name:
                inst = test

        if inst == None:
            print('Cannot fit to: ' + test_name)
            print(test_name + ' not found in active suite!')

        # Pass test instance to agents defined fitting function
        return self.agent.fit_to(inst)

    def test_to(self, test_name, iters):
        # Make sure agent exists
        if self.agent == None:
            print('ERROR: No agent defined')
            return None

        # Search test suite for test
        inst = None
        for test in self.test_suite:
            if test_name == test.header.env_name:
                inst = test

        # Run the test in the environment
        # TODO: Move testing to AIQ side and not ENV side
        return self.agent.test_to(inst, iters)


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

        return f_score

    # Called for dataset tests
    def ds_test(self, test):
        test_data = test.get_test()
        predictions = self.agent.predict(test.header, test_data)
        score = test.evaluate(predictions)

        f_score = self.norm(score, 
                            test.header.env_min_score, 
                            test.header.env_max_score)

        return f_score

    # Score normalization
    def norm(self, score, min_s, max_s):
        # Normalize score
        norm_score = (score - min_s) / (max_s - min_s)
        
        # catchall incase score doesnt get normalized
        if norm_score > 1.0:
            return 1.0
        else:
            return norm_score


    # Fun animation!
    def animation(self, start_text, end_text):
        t = threading.Thread(target=self.util_animation, 
                             args=(start_text, end_text,))
        t.start()

    # Fun animation (thread function)
    def util_animation(self, start_text, end_text):
        self.stop_animation_bool = False  
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.stop_animation_bool:
                break
            print('\r' + start_text + ' ' + c, end='')
            time.sleep(0.15)
        print('\r' + end_text + ' ', end='')
        self.stop_animation_bool = False      

    def stop_animation(self):
        self.stop_animation_bool = True 


    # Logging utility
    # Expects a results history
    def fancy_logger(self, name, results, file_name='data', write='a'):
        with open(file_name + '.csv', write, newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            res = results['episode_reward'][-20:]
            avg = sum(res) / len(res)
            stdev = statistics.stdev(res)
            spamwriter.writerow((name, len(res),avg, -1*stdev, stdev, *res))





