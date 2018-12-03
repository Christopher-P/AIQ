import json
import requests

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

