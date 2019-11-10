import json
import requests

class backend_handler():

    # Username and password required for logging to AIQ website
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
        self.call_rest("not_empty", str_data)

        # Handle website
        # TODO: Fix on server end
        if 'div' in self.response.text:
            text = "Account information not found, make sure to sign up at https://portal.eecs.wsu.edu/aiq"
        else:
            text = "Submission made succesfully! ="

        ## Formatting, so doesnt look terrible
        #text = self.response.text.replace('\\', '')
        return text

    # This function will accept entries for the db
    # Accepts Epochs, Params
    def send_complexity(self, test_name, epochs, params):
        data  = "'" + str(test_name) + "' "
        data += "'" + str(epochs) + "' "
        data += "'" + str(params) + "' "
        self.call_rest("Complexity", data)
        return self.response

    def connect(self):
        self.call_rest("Connect", 1)
        if(self.response.text == '\"Connection Successful\"'):
            return True
        else:
            return False

    def call_rest(self, option, data):
        url = 'https://portal.eecs.wsu.edu/aiq/index.php/rest/'
        data = {
            "username"  : self.username,
            "password"  : self.password,
            "option"    : option,
            "data"      : data
        }
        self.response = requests.post(url, data=json.dumps(data))

