import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [9.9646, 8.0395, 9.8378, 9.4667, 12.9097, 13.8024, 12.8772, 9.7287, 12.5569, 12.2871]
mse = [0.6511, 0.3508, 0.2877, 0.4525, 0.4172, 0.2871, 0.3156, 0.4421, 0.4375, 0.5128]

number_of_domains = 10

# Normalize everything to sum=1
sum_mse = sum(mse)
sum_auc = sum(auc)
for ind in range(number_of_domains):
    mse[ind] = mse[ind]/sum_mse
    auc[ind] = auc[ind]/sum_auc

# Find SE from mse (RMSE functionally equaivalent to STDEV)
standard_error = []
for i in range(number_of_domains):
    standard_error.append(1.96 * math.sqrt(mse[i]) / math.sqrt(1000))

means = np.asarray(auc)

# create stacked errorbars:
# Main bars
plt.errorbar(np.arange(10, 110, step=10), means, yerr=[standard_error, standard_error],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)

# Trendline
z = np.polyfit(np.arange(10, 110, step=10), means, 1)
p = np.poly1d(z)
x = np.arange(10, 110, step=10)
plt.plot(x, p(x), color='black')

# Formatting
plt.xlim(5, 105)
#plt.ylim(0, 0.5)
plt.xlabel('Classes')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Classes.png')
