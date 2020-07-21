import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [2.3955, 2.3003, 5.9905, 5.283, 5.0384, 5.3465, 4.6682, 4.4953, 4.6682, 5.6246, 3.9753, 6.81, 4.6074, 5.6986, 5.4895, 4.3099, 5.1849, 5.9141, 5.9489, 5.2473]
mse = [2.9032, 6.4379, 4.211, 5.146, 2.1633, 2.5945, 1.7093, 3.2531, 5.8428, 2.956, 3.8241, 1.6394, 3.7085, 1.7095, 3.4702, 4.786, 1.9169, 3.589, 5.308, 3.4734]




grav = ['0.0', '2.45', '4.9', '7.3500000000000005', '9.8', '12.25', '14.700000000000001', '17.150000000000002', '19.6', '22.05', '24.5', '26.950000000000003', '29.400000000000002', '31.85', '34.300000000000004', '36.75', '39.2', '41.650000000000006', '44.1', '46.550000000000004']

for ind,val in enumerate(grav):
    grav[ind] = float(val)

x = grav

number_of_domains = len(auc)

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
plt.errorbar(x, means, yerr=[standard_error, standard_error],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)

# Trendline
z = np.polyfit(x, means, 2)
p = np.poly1d(z)

plt.plot(x, p(x), color='black')

# Formatting
plt.xlim(-0.5, 47)
plt.ylim(0, 0.15)
plt.xlabel('Gravity')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Distance.png')
