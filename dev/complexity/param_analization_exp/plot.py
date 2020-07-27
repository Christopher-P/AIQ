import matplotlib.pyplot as plt
import numpy as np
import math

# Gravity data
''' 
# Generated from model_fit.py
auc = [2.3955, 2.3003, 5.9905, 5.283, 5.0384, 5.3465, 4.6682, 4.4953, 4.6682, 5.6246, 3.9753, 6.81, 4.6074, 5.6986, 5.4895, 4.3099, 5.1849, 5.9141, 5.9489, 5.2473]
mse = [2.9032, 6.4379, 4.211, 5.146, 2.1633, 2.5945, 1.7093, 3.2531, 5.8428, 2.956, 3.8241, 1.6394, 3.7085, 1.7095, 3.4702, 4.786, 1.9169, 3.589, 5.308, 3.4734]
grav = ['0.0', '2.45', '4.9', '7.3500000000000005', '9.8', '12.25', '14.700000000000001', '17.150000000000002', '19.6', '22.05', '24.5', '26.950000000000003', '29.400000000000002', '31.85', '34.300000000000004', '36.75', '39.2', '41.650000000000006', '44.1', '46.550000000000004']
'''
'''
# Force Data
auc = [5.211, 5.0548, 3.4999, 3.8176, 4.5915, 4.0052, 3.9577, 3.81, 4.1847, 3.9362, 3.7805, 5.3837, 4.4498, 4.7314, 6.5905, 6.1185, 6.7111, 4.8393, 5.7308, 5.2097]
mse = [4.4901, 1.0949, 1.1094, 1.3685, 3.0733, 0.154, 0.6689, 1.4322, 0.3585, 1.1033, 3.2368, 1.458, 3.6651, 2.7627, 4.3426, 2.2159, 3.2539, 1.1157, 2.0571, 2.1244]
grav = ['0.25', '0.5', '0.75', '1.0', '1.25', '1.5', '1.75', '2.0', '2.25', '2.5', '2.75', '3.0', '3.25', '3.5', '3.75', '4.0', '4.25', '4.5', '4.75', '5.0']
'''
# Force data
auc = [3.5985, 4.3234, 3.5599, 3.8474, 4.0914, 3.6421, 4.0953, 4.0234, 4.1308, 3.67, 3.6726, 6.5905, 5.1497, 4.0552, 4.8237, 4.2241, 5.1497, 5.9904, 4.3752, 4.6054]
mse = [1.4374, 1.2807, 2.65, 1.275, 1.2581, 0.7002, 0.3973, 1.269, 0.7135, 1.2148, 1.725, 3.0207, 4.0627, 1.212, 3.1825, 0.7641, 2.3344, 2.4728, 0.7421, 2.4321]
grav = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']

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
plt.xlim(min(grav)-0.1, max(grav)+0.1)
plt.ylim(0.0, 0.1)
plt.xlabel('Force')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Force.png')
