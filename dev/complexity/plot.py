### Used to plot experimental results from run.py
import csv
import numpy as np
from scipy.stats import pearsonr
from numpy import mean
import matplotlib.pyplot as plt
import ast
import sys
maxInt = sys.maxsize
csv.field_size_limit(maxInt)

import math
def load_file(filename):
    data = []
    with open('data/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        c = 0
        for row in spamreader:
            # We have 2 duplicates :(
            if c < 2:
                c = c + 1
                continue
            data.append((row[0], ast.literal_eval(row[1])))

    return data


data = load_file('RAW.csv')

# 90% vals
max_vals = {'CartPole-v0'   :[180.0, False], 
          'CartPole-v1'     :[450.0, False],
          'Acrobot-v1'      :[-110.0, False],
          'MountainCar-v0'  :[180.0, False],
          'Roulette-v0'     :[0.0, True],     # avg 
          'FrozenLake-v0'   :[0.9, True],    # avg 
          'CliffWalking-v0' :[-170.0, False], 
          'NChain-v0'       :[900.0, False], 
          'FrozenLake8x8-v0':[0.9, True],     # avg
          'Taxi-v2'         :[-180.0, False]}

# 100%
max_vals = {'CartPole-v0'   :[200.0, False], 
          'CartPole-v1'     :[500.0, False],
          'Acrobot-v1'      :[-42.0, False],
          'MountainCar-v0'  :[-110.0, False],
          'Roulette-v0'     :[0.0, True],     # avg 
          'FrozenLake-v0'   :[1.0, True],    # avg 
          'CliffWalking-v0' :[-10.0, False], 
          'NChain-v0'       :[3677.0, False], 
          'FrozenLake8x8-v0':[1.0, True],     # avg
          'Taxi-v2'         :[9.7, False]}

max_vals_arr = [200.0, 500.0, -42.0, -110.0, 0.0, 1.0, -10.0, 3677.0, 1.0, 9.7]

min_vals = []

scores = []
samples = 50

print(max(data[4][1]['episode_reward']))

# Find minimum values
for ind, i in enumerate(data):
    print(i[0])

    # Do avg
    if max_vals[i[0]][1] == True:
        tmp_arr = i[1]['episode_reward'][0:samples]
        min_avg = 999999999
        c = 0
        for j in i[1]['episode_reward'][samples:]:
            if sum(tmp_arr)/len(tmp_arr) < min_avg:
                min_avg = sum(tmp_arr)/len(tmp_arr)
            tmp_arr[c] = j
            c = c + 1
            if c >= samples:
                c = 0
        min_vals.append(min_avg)
        continue
            
    # Simple max
    min_vals.append(min(i[1]['episode_reward']))
    #plt.scatter(i[1]['nb_steps'], i[1]['episode_reward'])
    #plt.show()

print(min_vals)

# Find generated values
for ind, i in enumerate(data):
    print(i[0])

    # Do avg
    if max_vals[i[0]][1] == True:
        tmp_arr = i[1]['episode_reward'][0:samples]
        max_avg = -999999999
        c = 0
        for j in i[1]['episode_reward'][samples:]:
            if sum(tmp_arr)/len(tmp_arr) > max_avg:
                max_avg = sum(tmp_arr)/len(tmp_arr)
            tmp_arr[c] = j
            c = c + 1
            if c >= samples:
                c = 0
        scores.append(max_avg)
        continue
            
    # Simple max
    scores.append(max(i[1]['episode_reward']))
    #plt.scatter(i[1]['nb_steps'], i[1]['episode_reward'])
    #plt.show()
print(scores)

n_scores = []

# Find normed values (will give percentage of max)
for i in range(10):
    
    normed_val = (scores[i] - min_vals[i]) / (max_vals_arr[i] - min_vals[i])
    n_scores.append(normed_val)

# Final normed scores (mostly normder to 0-1)
print (n_scores)
exit()

# Generate simple bar plot
names = ["CartPole-v0", "CartPole-v1", "Acrobot-v1",
        "MountainCar-v0", "Roulette-v0","FrozenLake-v0",
         "CliffWalking-v0","NChain-v0","FrozenLake8x8-v0", "Taxi-v2"]


n_scores, names = (list(t) for t in zip(*sorted(zip(n_scores, names))))
print(n_scores, names)


plt.bar(range(10), n_scores, align='center', alpha=0.5)
plt.xticks(range(10), names)
plt.ylabel('Percentage of max')
plt.title('Test Suite')

plt.show()


