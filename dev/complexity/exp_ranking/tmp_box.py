import matplotlib.pyplot as plt
import numpy as np
import math

auc = [88.02, 85.13, 136.8, 194.66, 86.43]
mse = [0.62, 0.64, 1.31, 0.75, 1.19]

# Find max
auc_max = []
auc_min = []
for i in range(5):
    auc_max.append(auc[i] + (100 * mse[i]))
    auc_min.append(auc[i] - (100 * mse[i]))

# Norm them
sum_auc_max = sum(auc_max)
sum_auc_min = sum(auc_min)
sum_auc = sum(auc)
sum_mse = sum(mse)
for ind in range(5):
    auc_max[ind] = auc_max[ind]/sum_auc_max
    auc_min[ind] = auc_min[ind]/sum_auc_min
    auc[ind] = auc[ind]/sum_auc
    mse[ind] = mse[ind]/sum_mse
    
#for ind in range(5):
#    mse[ind] = math.sqrt(mse[ind]) * 10



entropy_n = [182532.4206179811,
211904.015471518,
269661.94757943094,
434866.9281534464,
50090.15641089917]

e_s = sum(entropy_n)
for ind, val in enumerate(entropy_n):
    entropy_n[ind] = val/e_s
    print(round(entropy_n[ind],4))

# construct some data like what you have:

mins = auc_min
maxes = auc_max
means = np.asarray(auc)
std = np.asarray(mse)

# create stacked errorbars:
#plt.errorbar(np.arange(5), means, std, fmt='ok', lw=3)
plt.errorbar(np.arange(5), means, [means - mins, maxes - means],
             fmt='.k', ecolor='gray', lw=1)
plt.scatter(np.arange(5), entropy_n, color='r', marker=',')
plt.legend(['Entropic Prediction', 'Empirical Prediction'])
plt.xlim(-0.5, 4.5)
plt.ylim(0, 0.5)

plt.show()
