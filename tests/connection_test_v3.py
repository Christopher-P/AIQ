import sys
sys.path.insert(0, "/home/chris/Desktop/github/AIQ")

import yaml
import time

from AIQ.backend import *

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():

    username = credentials['username']
    password = credentials['password']
    data = "'username' 'christopher_Pereyda' 'BL_RPM' '1.0' 'hello' 'hi'"
    test_name = "Not Connection"


    back = backend_handler(username, password, "", "")
    back.call_rest(username, password, data, test_name, env_name="")
    print(back.response)
    print(back.response.text)

    exit()



if __name__ == '__main__':
    main()



