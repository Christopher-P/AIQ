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

    back = Backend_DS(username, password)
    
    #Check login data
    if not back.connect():
        print("Invalid login Credentials")
        exit()

    print("Credentials Verified")
    exit()

if __name__ == '__main__':
    main()
