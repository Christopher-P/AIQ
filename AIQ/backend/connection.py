import json
import requests

class backend_handler():

    def __init__(self, username, password):
        self.username  = username
        self.password  = password
        self.response  = None

    def submit(self, data):
        # Format data here for submission!
        str_data = "'USERNAME' '" + self.username + "' "
        for key, values in data.items():
            str_data += "'"
            str_data += str(key)
            str_data += "'"
            str_data += " "
            str_data += "'"
            str_data += str(values)
            str_data += "'"
            str_data += " "
        # Remove last space
        str_data = str_data[:-1]

        # Send information to rest handler
        self.call_rest(self.username, self.password, "not_empy", str_data)
        return self.response.text

    def connect(self):
        self.call_rest(self.username, self.password, "Connect", 1)
        if(self.response.text == '\"Connection Successful\"'):
            return True
        else:
            return False


    def call_rest(self, username, password, option, data):
        url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
        data = {
            "username"  : username,
            "password"  : password,
            "option"    : option,
            "data"      : data
        }
        self.response = requests.post(url, data=json.dumps(data))

