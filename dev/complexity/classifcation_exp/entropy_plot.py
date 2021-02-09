import matplotlib.pyplot as plt
import numpy as np
import math
import csv
import statistics
from scipy.stats import sem

data = dict()

with open('results_model_fit.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        name = row[0]
        score = float(row[1])

        if name not in data.keys():
            data[name] = []

        data[name].append(score)

# Generated from model_fit
auc = []
se = []
names = ["MNIST", "FMNIST", "C10", "C100", "CARTPOLE"]
for name in names:
    auc.append(sum(data[name])/len(data[name]))
    se.append(sem(data[name]))
    print(name, auc[-1])
    print(name, statistics.stdev(data[name]))

# Generated from entropy.py
entropy = [182532.4206179811,
211904.015471518,
269661.94757943094,
434866.9281534464,
50090.15641089917]

# Normalize everything to 0,1
entropy = [float(i)/max(entropy) for i in entropy]
#k = max(auc)
auc = [float(i)/max(auc) for i in auc]

for ind, val in enumerate(se):
    se[ind] = val / 1.0 #k
print(se)

# create stacked errorbars:
# Main bars
plt.errorbar(np.arange(5), auc, yerr=[se, se],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)
# Entropy points
plt.scatter(np.arange(5), entropy, color='r', marker=',')
#plt.scatter(np.arange(6), means, color='black', marker='.')

# Formatting
plt.legend(['Entropic Prediction', 'Complexity Measure'])
plt.xlim(-0.5, 5.5)
plt.xticks(np.arange(6), ["MNIST", "FMNIST", "C10", "C100", "CARTPOLE", "CARTPOLE-RL"], rotation=12)
plt.ylim(0, 1.5)
plt.xlabel('Tasks')
plt.ylabel('Complexity / Entropy')

# Manuel editing needed to ensure x-label is not cutoff
plt.show()

# Save to file
#plt.savefig('Entropies.png')
