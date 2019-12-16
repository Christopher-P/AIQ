# Used to find the scaling ratio based on data in raw

import csv
import ast

# Standard load function
def load_file(filename):
    data = []
    with open('data_bak/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        for row in spamreader:
            data.append((row[0], row[1], row[2], row[3]))

    return data

# returns a scale factor to be used later
def get_scales(data):
    #print(data)
    scales = []
    
    # We have 10 tests
    for i in range(10): 
        # Initial values 
        min_r = 99999999999999
        max_r = -9999999999999  

        # We have 10 tests
        for j in range(10):
            scores= data[i + j*10]
            

            # find min max scores for test
            if min(scores) < min_r:
                min_r = min(scores)
            if max(scores) > max_r:
                max_r = max(scores)

        scales.append((min_r, max_r))
    
    print(scales)
    return scales

data = load_file('RAW.csv')
found = True



raw_l = []


for entry in data:
    # We have one extra of these from running the experiment
    if entry[0] == 'FrozenLake8x8-v0' and entry[1] == "CliffWalking-v0" and found:
        found = False
        continue
    raw = ast.literal_eval(entry[3])
    raw_l.append(raw['episode_reward'])

print(len(raw_l))
get_scales(raw_l)
