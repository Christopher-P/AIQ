import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from model_fit.py
auc = [5.441, 18.2665, 4.1411, 4.922, 12.0947, 7.9286, 8.04, 7.202, 6.6639, 6.5013, 6.2348, 7.2213, 5.7164, 6.2969, 5.697, 5.8069, 5.552, 5.587, 5.69, 5.7445]
mse = [2.9868, 2.5725, 1.2721, 0.9474, 1.2529, 1.1477, 1.2527, 1.1159, 1.3252, 1.3744, 1.4478, 1.4873, 1.231, 1.2136, 1.4452, 1.6062, 1.8803, 1.2004, 1.5011, 1.6519]


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
