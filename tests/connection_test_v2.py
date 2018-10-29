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

    back = backend_connector()
    back.call_rest(username, password, 1, "Connect")

    exit()

if __name__ == '__main__':
    main()
