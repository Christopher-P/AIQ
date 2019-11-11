# Used to list all of the currently implemented tests
# in the test suite

# Used for loading tests into test suite
import importlib

class tests():

    def __init__(self):
        self.suites = []
        self.env_names = []

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
            for entry in all_envs:
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
        self.load_gym()
        return self.suites, self.env_names


class test_loader():

    def __init__(self):
        return None

    def load(self):
        return None

    # Add a test to the test suite
    def add(self, env_name, params=None):
        #print(env_name)
        # https://stackoverflow.com/questions/547829/
        try:
            mod = __import__('AIQ.test_suite', fromlist=[env_name])
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
    def add_all_tests(self, ignore):
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
                if self.add(suites[ind], {'env_name':test_names[ind]}):
                    self.suites_added.append(suites[ind])
                    self.test_names.append(test_names[ind])

        return self.suites_added













