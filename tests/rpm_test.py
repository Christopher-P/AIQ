import sys
sys.path.insert(0, "/home/chris/Desktop/github/AIQ")

import yaml
import time

from AIQ.test_suite import RPM

#Import username and password
credentials = yaml.safe_load(open("credentials.yml"))

def main():
  #***** Begin RPM Example **********#
    username = credentials['username']
    password = credentials['password']
    AIQ_RPM = RPM(username, password)
    
    #Check login data
    if not AIQ_RPM.connect():
        print("Invalid login Credentials")
        exit()
    
    # Request data from RPM generator (max 750)
    results_train = AIQ_RPM.get_train([750, 4])
    print(results_train)
    
    # Request data that needs a solution
    results_test = AIQ_RPM.get_test(4)
    print(results_test)
    
    #Submit a solution
    data = '"[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]"'
    print(AIQ_RPM.submit(data))
    
    exit()

if __name__ == '__main__':
    main()
