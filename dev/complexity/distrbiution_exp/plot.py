import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [4.9561, 5.0855, 5.1566, 4.7356, 5.01, 4.9154, 5.3037, 5.2821, 5.0967, 5.597, 4.8653, 6.3123, 5.7874, 6.5714,
       5.0238, 6.149, 5.9376, 6.0853, 5.9871, 6.5085]

mse = [1.6069, 2.0549, 1.4217, 1.8377, 1.5756, 1.2339, 1.404, 1.6713, 1.774, 1.3187, 1.8169, 1.2732, 1.5557, 1.5664,
       1.9309, 1.9535, 2.5924, 2.4992, 2.5626, 2.7055]

# Generated from overlap.py
over = [0.9698, 0.8058, 0.6718, 0.5503, 0.44, 0.3494, 0.2802, 0.2214, 0.1743, 0.1426, 0.1099, 0.086, 0.0684, 0.0529,
        0.0419, 0.0313, 0.0241, 0.0179, 0.0141, 0.0107]
# Flip over
over = list(reversed(over))

# Generated from model_fit.py
distance = [0.0, 0.1581138830084191, 0.31622776601683805, 0.4743416490252568, 0.6324555320336757, 0.7905694150420949,
            0.948683298050514, 1.106797181058933, 1.2649110640673515, 1.4230249470757705, 1.5811388300841898,
            1.7392527130926088, 1.897366596101028, 2.055480479109446, 2.2135943621178655, 2.3717082451262845,
            2.529822128134704, 2.6879360111431225, 2.846049894151541, 3.0041637771599605]
distance = list(reversed(distance))

print(len(auc), len(mse), len(distance))

# Change here for dif x-axis
#x = over
x = distance

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
#plt.errorbar(x, means, yerr=[standard_error, standard_error],
#             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)

plt.scatter(x, means, color='black', marker='.')

# Trendline
z = np.polyfit(x, means, 2)
p = np.poly1d(z)

plt.plot(x, p(x), color='black')
#plt.scatter(x, over, color='red')

# Formatting
#plt.xlim(-0.1, 3.1)
plt.xlabel('Cluster Center Distance')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Distance.png')
