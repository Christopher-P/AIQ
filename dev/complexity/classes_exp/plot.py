import matplotlib.pyplot as plt
import numpy as np
import math

from scipy.optimize import curve_fit

# Generated from model_fit.py
auc = [9.3979, 10.5648, 11.1701, 11.5362, 12.0138, 12.3153, 12.4202, 12.6515, 12.8786, 13.0363]
mse = [0.5618, 0.5782, 0.5974, 0.6064, 0.6081, 0.7243, 0.6826, 0.6723, 0.6453, 0.7036]
number_of_domains = 10

# Normalize everything to sum=1
tmp = max(auc)*len(auc)
auc = [float(i)/max(auc) for i in auc]
mse = [float(i)/tmp for i in mse]
    
# Find SE from mse (RMSE functionally equaivalent to STDEV)
standard_error = []
for i in range(number_of_domains):
    standard_error.append(1.96 * math.sqrt(mse[i]))

# create stacked errorbars:
# Main bars
plt.errorbar(np.arange(10, 110, step=10), auc, yerr=[standard_error, standard_error],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)

# Trendline 1
x = np.arange(0, 110, step=1)
z = np.polyfit(np.arange(10, 110, step=10), auc, 2)
p = np.poly1d(z)
plt.plot(x, p(x), color='black')

# Formatting
plt.xlim(5, 105)
#plt.ylim(0, 0.12)
plt.xlabel('Classes')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Classes.png')
