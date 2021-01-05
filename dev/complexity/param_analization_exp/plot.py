import matplotlib.pyplot as plt
import numpy as np
import math

# Gravity data

# Generated from model_fit.py
'''
auc = [3.5984, 4.0194, 4.2322, 4.0122, 3.7949, 3.9532, 3.7849, 4.0725, 4.3933, 5.0773, 4.5117, 4.2933, 4.996, 4.0885, 4.3506, 4.9804, 5.9427, 4.902, 5.3871, 4.0765]
mse = [2.9032, 6.4379, 4.211, 5.146, 2.1633, 2.5945, 1.7093, 3.2531, 5.8428, 2.956, 3.8241, 1.6394, 3.7085, 1.7095, 3.4702, 4.786, 1.9169, 3.589, 5.308, 3.4734]
grav = ['0.0', '2.45', '4.9', '7.3500000000000005', '9.8', '12.25', '14.700000000000001', '17.150000000000002', '19.6', '22.05', '24.5', '26.950000000000003', '29.400000000000002', '31.85', '34.300000000000004', '36.75', '39.2', '41.650000000000006', '44.1', '46.550000000000004']
'''
'''
# Pole Length Data
auc = [5.2143, 5.0591, 3.5798, 3.9383, 4.5921, 4.1647, 4.1164, 3.9861, 4.3903, 4.1267, 3.7812, 5.3809, 4.451, 4.7345, 6.5964, 6.1176, 6.7132, 4.8388, 5.7302, 5.2121]
mse = [4.4901, 1.0949, 1.1094, 1.3685, 3.0733, 0.154, 0.6689, 1.4322, 0.3585, 1.1033, 3.2368, 1.458, 3.6651, 2.7627, 4.3426, 2.2159, 3.2539, 1.1157, 2.0571, 2.1244]
grav = ['0.25', '0.5', '0.75', '1.0', '1.25', '1.5', '1.75', '2.0', '2.25', '2.5', '2.75', '3.0', '3.25', '3.5', '3.75', '4.0', '4.25', '4.5', '4.75', '5.0']
'''

# Force data
auc = [3.8393, 4.5677, 3.7063, 4.0717, 4.1868, 3.7468, 4.208, 4.1473, 4.2342, 3.7454, 3.7433, 6.5923, 5.1529, 4.1365, 4.8279, 4.3119, 5.1508, 5.9955, 4.4513, 4.6955]
mse = [1.4374, 1.2807, 2.65, 1.275, 1.2581, 0.7002, 0.3973, 1.269, 0.7135, 1.2148, 1.725, 3.0207, 4.0627, 1.212, 3.1825, 0.7641, 2.3344, 2.4728, 0.7421, 2.4321]
grav = ['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0']

for ind,val in enumerate(grav):
    grav[ind] = float(val)

x = grav

number_of_domains = len(auc)

# Normalize everything to sum=1
tmp = max(auc)*max(mse)*len(auc)
auc = [float(i)/max(auc) for i in auc]
mse = [float(i)/tmp for i in mse]

# Find SE from mse (RMSE functionally equaivalent to STDEV)
standard_error = []
for i in range(number_of_domains):
    standard_error.append(1.96 * math.sqrt(mse[i]))

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
#plt.ylim(0.0, 0.1)
plt.xlabel('Gravity')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Gravity.png')
