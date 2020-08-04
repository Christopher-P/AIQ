import csv

import numpy as np

from sklearn.svm import SVR, SVC
from sklearn.covariance import ShrunkCovariance
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

import scipy as sp

import matplotlib.pyplot as plt
from statistics import stdev
import ast
import math

with open('data/results.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # centers, nodes, layers, TP, NTP, score
    results = dict()
    c = 0
    datum  = []
    avg = 0
    for row in spamreader:
        nodes  = int(row[1])
        layers = int(row[2])
        TP     = int(row[3])
        score  = float(row[5])

        datum.append(score)

        if c >= 4:        
            c = 0
            amount = nodes * layers
            # Check if it already exists
            if amount not in results:
                results[amount] = []

            results[amount].append(datum)
            datum  = []
        else:
            c = c + 1


# Many plots data cleaning function
def clean(TP, means):
    # Make a set of all tp values
    tps = set()
    for i in TP:
        tps.add(i)
    print(tps)

    # Find mean (y) and stderror of data
    y = []
    stds = []
    for i in tps:
        numbers = []
        for ind,val in enumerate(TP):
            # Check for correct tp
            if i != val:
                continue

            # Append if correct
            numbers.append(means[ind])

        # Compute stderror
        if len(numbers) == 1:
            stds.append(0.0)
        else:
            stderror = stdev(numbers) / math.sqrt(len(numbers))
            conf_int = 1.96 * stderror
            stds.append(conf_int)

        # Compute mean of means
        mega_mean = sum(numbers) / len(numbers)
        y.append(mega_mean)

    return list(tps), y, stds

# Overall Plot
TPS = []
means = []
stds = []
once = 0
# Many dots plot
for TP in results.keys():
    for sample in results[TP]:
        # Const complexity from calibration
        comps = [0.1693, 0.1638, 0.2632, 0.3745, 0.0292]

        # Multiply element wise
        #scores = np.multiply(comps, sample)
        scores = sample
        
        TPS.append(TP)        
        means.append(np.sum(scores))
        markers = ['x'] * 5

        x = [TP] * 5
        y = scores
        s = ['8', 's', 'p', 'D', 'X']
        col = ['red','green','blue', 'brown','orange']
        label = ['MNIST', 'FMNIST', 'C10', 'C100', 'CARTPOLE']
        for _s, c, _x, _y, _l in zip(s, col, x, y, label):
            if once < 5:
                plt.scatter(_x, _y, marker=_s, c=c, label=_l)
                once = once + 1
            else:
                plt.scatter(_x, _y, marker=_s, c=c)
        #plt.scatter([TP] * 5, scores, marker=markers)
plt.legend()
plt.xlabel('nodes * layers')
plt.ylabel('SCORE')
plt.show()




# Clean data
x, y, std = clean(TPS, means)

######
# create stacked errorbars:
# Main bars
plt.errorbar(x, y, yerr=[std, std],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1, label='Mean/Error')

'''
# Trendline
z = np.polyfit(np.exp(x), np.exp(y), 1)
print(z)
p = []
for i in x:
    k = np.log(z[1]) * np.log(i * z[0])
    p.append(k)

plt.plot(x, p, color='black')
'''

def binding(x,kd,bmax):
    return (bmax*x)/(x+kd)
param=sp.optimize.curve_fit(binding, x,y)

plt.plot(np.arange(36), binding(np.arange(36),*param[0]), color='orange', label='TrendLine')

# Single points plot
plt.scatter(TPS, means, marker='x', label='Scores')
plt.legend(loc='lower right')
plt.xlabel('nodes * layers')
plt.ylabel('AIQ')
plt.show()


