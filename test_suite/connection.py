import json
import requests
from threading import Thread, Lock

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
        #print(results.text)
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
        