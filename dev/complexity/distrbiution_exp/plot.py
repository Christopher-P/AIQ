import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [5.441, 18.1083, 5.5733, 5.3867, 7.2495, 5.7799, 4.3935, 4.0923, 4.8699, 4.6452, 4.9111, 6.4134, 4.5814, 4.3172, 5.137, 4.773, 5.797, 4.2372, 4.7615, 4.4592]
mse = [3.0413, 2.5981, 1.275, 1.0541, 1.4604, 1.4957, 1.3555, 1.1132, 1.4435, 1.3915, 1.6932, 1.3368, 1.4956, 1.7053, 1.2076, 1.6593, 1.1313, 1.609, 1.7217, 1.1933]



# Generated from overlap.py
over = [0.9698, 0.8058, 0.6718, 0.5503, 0.44, 0.3494, 0.2802, 0.2214, 0.1743, 0.1426, 0.1099, 0.086, 0.0684, 0.0529, 0.0419, 0.0313, 0.0241, 0.0179, 0.0141, 0.0107]


# Generated from model_fit.py
distance = [0.0, 0.1581138830084191, 0.31622776601683805, 0.4743416490252568, 0.6324555320336757, 0.7905694150420949, 0.948683298050514, 1.106797181058933, 1.2649110640673515, 1.4230249470757705, 1.5811388300841898, 1.7392527130926088, 1.897366596101028, 2.055480479109446, 2.2135943621178655, 2.3717082451262845, 2.529822128134704, 2.6879360111431225, 2.846049894151541, 3.0041637771599605]

print(len(auc), len(mse), len(distance))

x = distance
number_of_domains = len(auc)

# Normalize everything to sum=1
sum_mse = sum(mse)
sum_auc = sum(auc)
sum_over = sum(over)
for ind in range(number_of_domains):
    mse[ind] = mse[ind]/sum_mse
    auc[ind] = auc[ind]/sum_auc
    over[ind] = over[ind]/sum_over

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
plt.scatter(x, over, color='red')

# Formatting
plt.xlim(-0.1, 3.1)
plt.ylim(0, 0.2)
plt.xlabel('Cluster Distance')
plt.ylabel('Complexity')

# Save to file
plt.savefig('Distance.png')
