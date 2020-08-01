import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [6.0822, 5.6765, 5.6473, 5.2732, 4.7789, 4.458, 4.6108, 4.0686, 4.1759, 4.2632, 4.2129, 4.1003, 4.1281, 4.262, 4.2501, 4.544, 4.5879, 5.4438, 5.441, 5.1775]
mse = [1.6069, 2.0549, 1.4217, 1.8377, 1.5756, 1.2339, 1.404, 1.6713, 1.774, 1.3187, 1.8169, 1.2732, 1.5557, 1.5664, 1.9309, 1.9535, 2.5924, 2.4992, 2.5626, 2.7055]

# Generated from overlap.py
over = [0.9698, 0.8058, 0.6718, 0.5503, 0.44, 0.3494, 0.2802, 0.2214, 0.1743, 0.1426, 0.1099, 0.086, 0.0684, 0.0529, 0.0419, 0.0313, 0.0241, 0.0179, 0.0141, 0.0107]


# Generated from model_fit.py
distance = [0.0, 0.1581138830084191, 0.31622776601683805, 0.4743416490252568, 0.6324555320336757, 0.7905694150420949, 0.948683298050514, 1.106797181058933, 1.2649110640673515, 1.4230249470757705, 1.5811388300841898, 1.7392527130926088, 1.897366596101028, 2.055480479109446, 2.2135943621178655, 2.3717082451262845, 2.529822128134704, 2.6879360111431225, 2.846049894151541, 3.0041637771599605]

print(len(auc), len(mse), len(distance))

# Change here for dif x-axis
x = over
#x = distance

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
    standard_error.append(1.96 * math.sqrt(mse[i])  / math.sqrt(1000))

means = np.asarray(auc)

# create stacked errorbars:
# Main bars
plt.errorbar(x, means, yerr=[standard_error, standard_error],
             fmt='.k', ecolor='black', lw=1, capsize=4, capthick=1)

# Trendline
z = np.polyfit(x, means, 2)
p = np.poly1d(z)

plt.plot(x, p(x), color='black')
#plt.scatter(x, over, color='red')

# Formatting
#plt.xlim(-0.1, 3.1)
plt.xlim(0.0, 1.0)
plt.ylim(0, 0.1)
plt.xlabel('Cluster Overlap')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Distance.png')
