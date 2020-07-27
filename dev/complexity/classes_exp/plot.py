import matplotlib.pyplot as plt
import numpy as np
import math

from scipy.optimize import curve_fit

# Generated from model_fit.py
auc = [12.7697, 14.2759, 15.4948, 15.8116, 16.005, 16.0625, 16.8369, 16.8693, 16.2225, 15.9173]
mse = [0.5618, 0.5782, 0.5974, 0.6064, 0.6081, 0.7243, 0.6826, 0.6723, 0.6453, 0.7036]
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
    standard_error.append(1.96 * math.sqrt(mse[i]) * (1/sum_mse) / math.sqrt(1000))

# create stacked errorbars:
# Main bars
plt.errorbar(np.arange(10, 110, step=10), auc, yerr=[standard_error, standard_error],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)

# Trendline
x = np.arange(10, 110, step=10)
z = np.polyfit(x, auc, 2)
p = np.poly1d(z)
plt.plot(x, p(x), color='black')

# Formatting
plt.xlim(5, 105)
#plt.ylim(0, 0.5)
plt.xlabel('Classes')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Classes.png')
