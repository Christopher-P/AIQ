import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [5.5035, 13.4004, 9.9669, 5.5493, 12.1891, 5.2608, 7.6815, 7.1215, 6.8174, 6.2868, 6.0218, 6.0987, 4.8191, 5.6892, 5.7414, 5.295, 5.8138, 5.1043, 5.5796, 6.0156]
mse = [3.3733, 1.5771, 1.2377, 1.7395, 1.5988, 1.072, 0.7998, 1.301, 0.5591, 1.7967, 0.8716, 1.8114, 2.0489, 0.653, 0.6669, 0.8612, 1.0166, 1.1058, 3.0428, 1.7059]


distance = [0.0, 0.1581138830084191, 0.31622776601683805, 0.4743416490252568, 0.6324555320336757, 0.7905694150420949, 0.948683298050514, 1.106797181058933, 1.2649110640673515, 1.4230249470757705, 1.5811388300841898, 1.7392527130926088, 1.897366596101028, 2.055480479109446, 2.2135943621178655, 2.3717082451262845, 2.529822128134704, 2.6879360111431225, 2.846049894151541, 3.0041637771599605]

x = distance

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
plt.xlim(-0.1, 3.1)
plt.ylim(0, 0.15)
plt.xlabel('Cluster Distance')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Distance.png')
