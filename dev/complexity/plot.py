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

# These scores were generated in tl/plot
Reward = [-9.71445146547012e-17, 0.0008628787288246648, -0.003869047619047619, 0.0, 0.004484551095126688, -0.0015515532630031494, 0.12241523862978626, 0.06831896551724148, 5.423421291365915e-05, -0.006730202960415738]
Ratio = [-0.01178415240644822, -0.001115716808150894, -1.0, 0.1, 0.023857919009226375, -0.1927710843373494, 0.2991826757206814, 0.20338983050847467, -0.05660377358490566, -0.024626021395740032]
JumpStart = [0.07317073170731707, 0.088, -0.15476190476190477, 0.0, -0.05581395348837209, 0.0, 0.16808797993440094, -0.025862068965517238, 0.0, -0.026946107784431128]
Asymptotic = [0.04878048780487804, 0.10239999999999999, 0.0, 0.0, -0.010232558139534886, 0.0, 0.04089523442021989, 0.04655172413793107, 0.0, 0.053892215568862284]

# Non normed scores
'''
Reward = [0.0, 0.21571968220619198, -0.3250000000000455, 0.0, 0.9641784854522994, -0.0015515532630031494, 3172.3909090909074, 31.700000000000045, 5.423421291365915e-05, -6.743663366336591]
Ratio = [-0.008395371113678461, -0.000883825487949535, 0.0008997119489860939, -0.0, -0.5064474944142994, -0.1927710843373494, -0.1694134646935516, 0.02482207341443747, -0.05660377358490566, 0.003982313282400185]
JumpStart = [18.0, 22.0, -13.0, 0.0, -12.0, 0.0, 4356.0, -12.0, 0.0, -27.0]
Asymptotic = [12.0, 25.6, 0.0, 0.0, -2.1999999999999997, 0.0, 1059.7999999999993, 21.59999999999991, 0.0, 54.0]
'''

print(np.corrcoef(n_scores, Reward))
print(np.corrcoef(n_scores,Ratio))
print(np.corrcoef(n_scores,JumpStart))
print(np.corrcoef(n_scores,Asymptotic))

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


