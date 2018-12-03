import json
import requests
from threading import Thread, Lock

# Implement on RPM to test
class backend_handler_RPM():

    def __init__(self, username, password):
        self.username = username
        self.password = password
    '''
    def get_train():

    def get_test():

    def submit():

    def connect():
    '''

# Implement generalized for other data
class backend_handler():

    def __init__(self, username, password, test_name, env_name):
        self.username  = username
        self.password  = password
        self.test_name = test_name
        self.env_name  = env_name
        self.response  = "EMPTY"

    def submit(self, data):
        self.call_rest(self.username, self.password, data, self.test_name, self.env_name)

    def connect(self):
        results = self.call_rest(self.username, self.password, 1, "Connect", self.env_name)
        print("here :" , self.response.text)

        if(results == '\"Connection Successful\"'):
            return True
        else:
            return False


    def call_rest(self, username, password, data, test_name, env_name):
        # t = Thread(target=self.sender, args=(username, password, data, test_name, env_name,))
        # t.start()
        self.sender(username, password, data, test_name, env_name)

    def sender(self, username, password, data, test_name, env_name):
        url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
        data = {
            "username"  : username,
            "password"  : password,
            "data"      : data,
            "test_name" : test_name,
            "env_name"  : env_name
        }
        
        self.response = requests.post(url, data=json.dumps(data))
        # self.response_handler()

    #def response_handler(self):
        # print(self.data)

class backend_handler_new():

    def __init__(self, username, password, test_name="EMPTY", env_name="EMPTY", response="EMPTY"):
        self.username  = username
        self.password  = password
        self.test_name = test_name
        self.env_name  = env_name
        self.response  = response

    def submit(self, data):
        self.call_rest(self.username, self.password, data, self.test_name, self.env_name)

    def connect(self):
        results = self.call_rest(self.username, self.password, 1, "Connect", self.env_name)
        print("here :" , self.response.text)

        if(self.response.text == '\"Connection Successful\"'):
            return True
        else:
            return False


    def call_rest(self, username, password, data, test_name, env_name):
        # t = Thread(target=self.sender, args=(username, password, data, test_name, env_name,))
        # t.start()
        self.sender(username, password, data, test_name, env_name)

    def sender(self, username, password, data, test_name, env_name):
        url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
        data = {
            "username"  : username,
            "password"  : password,
            "data"      : data,
            "test_name" : test_name,
            "env_name"  : env_name
        }
        
        self.response = requests.post(url, data=json.dumps(data))
        # self.response_handler()

    #def response_handler(self):
        # print(self.data)

'''
class Backend_DS():
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
                
    def get_train(self, amt, name):
        if amt[0] > 750:
            print("Cannot request more than 750 examples")
            return None
            
        data = None
        try:
            url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
            data = {
                "username"  : self.username,
                "password"  : self.password,
                "data"      : json.dumps(amt),
                "test_name" : name
            }
            # TODO 
            # Make verbose option
            print(url, data=json.dumps(data))
            
            data = requests.post(url, data=json.dumps(data)).text
            time.sleep(1)
        except:
            print("Failed to get data")
        finally:
            return data
            
    def get_test(self, name, n):
        data = None
        try:
            url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
            data = {
                "username"  : self.username,
                "password"  : self.password,
                "data"      : n,
                "test_name" : name
            }
            # TODO 
            # Make verbose option
            data = requests.post(url, data=json.dumps(data)).text
        except:
            print("Failed to get data")
        finally:
            self.data = data
            return data
    
    def submit(self, solution, name):
        try:
            url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
            data = {
                "username"  : self.username,
                "password"  : self.password,
                "data"      : solution,
                "test_name" : name
            }
            # TODO 
            # Make verbose option
            data = requests.post(url, data=json.dumps(data)).text
        except:
            print("Failed to get data")
        finally:
            return data
        
    #Return true if connection and credentials are good
    def connect(self):
        url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
        data = {
            "username"  : self.username,
            "password"  : self.password,
            "data"      : 1,
            "test_name" : "Connect"
        }
        results = requests.post(url, data=json.dumps(data))
        if(results.text == '\"Connection Successful\"'):
            return True
        else:
            return False
            
class Backend_RL():

    def __init__():
        print("dddd")
        
        
       
    # Utility function for sending batch of data
    def update_aiq(self, test_name, data):
        print("updating")
        try:
            url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
            data = {
                "username"  : self.username,
                "password"  : self.password,
                "data"      : data,
                "test_name" : test_name
                #"test_name" : "CartPole-v0"
            }
            
            self.update_amt = 0
            print(requests.post(url, data=json.dumps(data)).text)
            
        finally:
            self.updating = False
        



'''
