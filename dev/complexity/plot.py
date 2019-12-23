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
        for row in spamreader:
            data.append((row[0], ast.literal_eval(row[1])))

    return data


data = load_file('RAW.csv')

for i in data:
    print(max(i[1]['episode_reward']))
    plt.scatter(i[1]['nb_steps'], i[1]['episode_reward'])
    plt.show()

print(data[0])
