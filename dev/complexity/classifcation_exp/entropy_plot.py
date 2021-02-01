import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from plot.py
auc = [8.802, 8.513, 13.68, 19.466, 1.519, 2.7612]
mse = [0.62, 0.64, 1.31, 0.75, 1.99]

# Generated from entropy.py
entropy = [182532.4206179811,
211904.015471518,
269661.94757943094,
434866.9281534464,
50090.15641089917]

# Normalize everything to sum=1
'''
sum_mse = sum(mse)
sum_auc = sum(auc)
sum_entropy = sum(entropy)
for ind in range(5):
    mse[ind] = mse[ind]/sum_mse
    auc[ind] = auc[ind]/sum_auc
    entropy[ind] = entropy[ind]/sum_entropy
'''
# Normalize everything to 0,1
entropy = [float(i)/max(entropy) for i in entropy]
tmp = max(auc)*max(mse)*len(auc)
auc = [float(i)/max(auc) for i in auc]
mse = [float(i)/tmp for i in mse]
print(auc)
print(sum(auc))

#p = np.corrcoef(entropy, auc)
#print(p)

# Find SE from mse (RMSE functionally equaivalent to STDEV)
standard_error = []
for i in range(5):
    standard_error.append(1.96 * math.sqrt(mse[i]))

means = np.asarray(auc)

# create stacked errorbars:
# Main bars
#plt.errorbar(np.arange(5), means, yerr=[standard_error, standard_error],
#             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)
# Entropy points
plt.scatter(np.arange(5), entropy, color='r', marker=',')
plt.scatter(np.arange(6), means, color='black', marker='.')

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
