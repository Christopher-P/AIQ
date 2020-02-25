from .backend import backend_handler
from .test_suite.util import tests, test_loader

# Used for loading tests into test suite
import importlib

# Used for animations
import itertools
import threading
import time

# Used for logging results
import csv
import statistics 

class AIQ():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bl       = True
        self.backend  = backend_handler(self.username, self.password)

        self.current_test = ''
        self.current_percent = ''
        self.agent = None
        self.TL = test_loader()
        self.test_suite = []
        self.results = {}

    # Check connection
    def connect(self):
        return self.backend.connect()

    # Add a test to the test suite
    def add(self, env_name, params=None):
        t = self.TL.add(env_name, params)
        # Safety check for tests not found
        if t is not None:
            self.test_suite.append(t)
       
    # Add all available test envs to the suite
    def add_all_tests(self, ignore=None):
        # Use test loader
        t = self.TL.add_all_tests(ignore)

        # Safety check for tests not found
        for inst in t:
            if inst is not None:
                self.test_suite.append(inst)

        return None

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
        self.animation('Running test suite', 'Finished Test Suite!')
        for test in self.test_suite:
            test_name = test.get_header().env_name
            self.current_test = test_name

            # Seperate tests by RL or DS
            if test.get_header().rl == True:
                self.results[test_name] = self.rl_test(test)
            else:
                self.results[test_name] = self.ds_test(test)
            
            #print("res", test_name, self.results[test_name])
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
    def fit_to(self, inst):
        # Make sure agent exists
        if self.agent == None:
            print('ERROR: No agent defined')
            return None

        # Search test suite for test
        #inst = None
        #for test in self.test_suite:
        #    if test_name == test.header.env_name:
        #        inst = test

        if inst == None:
            print('Cannot fit to: ' + test_name)
            print(test_name + ' not found in active suite!')

        # Pass test instance to agents defined fitting function
        # Return history
        history = self.agent.fit_to(inst)
        return history

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
            self.current_percent = str(float(i) / trials * 100) + '%'
            test.reset()
            while test.done == False:
                observation = test.observation
                action = self.agent.act(test.header, observation)
                test.act(action)

            score += test.reward_total
        print(score, trials)

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
        elif norm_score < 0.0:
            return 0.0
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
            print('\r' + start_text + ' : ' + self.current_test + ' : ' + self.current_percent +'   '+ c, end='')
            if self.stop_animation_bool:
                break
        print("\033[K")
        print('-----------------')
        print(end_text)
        self.stop_animation_bool = False      

    def stop_animation(self):
        self.stop_animation_bool = True 
        time.sleep(0.2)


    # Logging utility
    # Expects a results history
    def fancy_logger(self, suite_name, env_name, results, file_name='data', write='a'):
        with open(file_name + '.csv', write, newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            avg = sum(results['episode_reward']) / len(results['episode_reward'])
            stdev = statistics.stdev(results['episode_reward'])
            spamwriter.writerow((suite_name, env_name, len(results['episode_reward']),
                                 avg, -1*stdev, stdev, *results['episode_reward']))





