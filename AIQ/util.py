# Used to list all of the currently implemented tests
# in the test suite

# Used for loading tests into test suite
import importlib

class tests():

    def __init__(self):
        self.suites = []
        self.env_names = []

        self.load_gym()
        self.load_vizdoom()

        return None
    


    def load_OBT(self):
        return None
    def load_AI2(self):
        return None
    def load_BW(self):
        return None

    def load_gym(self):
        # Get all OpenAIGym Envs        
        try:
            from gym import envs
            all_envs = envs.registry.all()
            exclude = ['atari','robotics','mujoco']
            for entry in all_envs:
                ex = False
                for name in exclude:
                    if name in entry._entry_point:
                        ex = True
                if not ex:
                    self.suites.append('OpenAIGym')
                    self.env_names.append(entry.id)
        except Exception as e:
            print(e)

    def load_vizdoom(self):
        # Get all default ViZDoom Envs        
        try:
            import vizdoom
            # Env name must match name in scenario folder!
            all_envs = ['basic', 'deadly_corridor', 'defend_the_center',
                        'defend_the_line', 'health_gathering', 
                        'predict_position', 'take_cover']
            for entry in all_envs:
                self.suites.append('ViZDoom')
                self.env_names.append(entry)
        except Exception as e:
            print(e)

    def load_RPM(self):
        return None
        
    def list_all(self):
        return self.suites, self.env_names


class test_loader():

    def __init__(self):
        return None

    def load(self):
        return None

    # Add a test to the test suite
    def add(self, env_name, params=None):
        # https://stackoverflow.com/questions/547829/
        try:
            mod = __import__('AIQ.test_suite.' + env_name, fromlist=[env_name])
            klass = getattr(mod, env_name)
            kless = getattr(klass, env_name)
            inst = kless(params)

            if params is not None and 'env_name' in params:
                print("{}: {} was added to the suite!".format(env_name, params['env_name']))
            else:
                print("{} was added to the suite!".format(env_name))
            return inst
        except Exception as e:

            print(e)
            if params is not None and 'env_name' in params:
                print("{}: {} was not found in the test_suite directory!".format(env_name, params['env_name']))
            else:
                print("{}  was not found in the test_suite directory!".format(env_name))
            return None

    # Add all available test envs to the suite
    # whitelist: test_name must be in whitelist to be added
    # blacklist: no part of black list must be in test_name
    def add_all_tests(self, whitelist, blacklist):
        # Used to hold instances of tests
        t_list = []

        # Class used to get the list of tests
        tests_class = tests()

        # Get test subsuites and env_names
        suites, test_names = tests_class.list_all()

        # Go through list and add each test
        for ind, val in enumerate(test_names):

            # Bool for handling logic with lists
            good = True
            
            # Handle whitelist
            if whitelist != None:
                good = False
                for white in whitelist:
                    if white in suites[ind] or white in test_names[ind]:
                        good = True
                        break

            # Handle blacklist
            if blacklist != None:
                for black in blacklist:
                    if black in suites[ind] or black in test_names[ind]:
                        good = False
                        break

            # Check if made past exclusions
            if good:
                # Add test
                t = self.add(suites[ind], {'env_name':test_names[ind]})
                # Append to list of test instances
                t_list.append(t)

        return t_list
