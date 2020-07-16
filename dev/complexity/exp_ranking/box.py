import matplotlib.pyplot as plt
import numpy as np
import math

# Generated from plot.py
auc = [8.802, 8.513, 13.68, 19.466, 1.519]
mse = [0.62, 0.64, 1.31, 0.75, 1.99]

# Find rmse from mse (functionally equaivalent to STDEV
rmse = []
for i in range(5):
    rmse.append(math.sqrt(mse[i]) / math.sqrt(1000))

# Norm them
sum_rmse = sum(rmse)
sum_auc = sum(auc)
sum_mse = sum(mse)
for ind in range(5):
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


print(rmse)
    
means = np.asarray(auc)
std = np.asarray(mse)

# create stacked errorbars:
#plt.errorbar(np.arange(5), means, std, fmt='ok', lw=3)
plt.errorbar(np.arange(5), means, yerr=[rmse, rmse],
             fmt='.k', ecolor='gray', lw=1)
plt.scatter(np.arange(5), entropy_n, color='r', marker=',')
plt.legend(['Entropic Prediction', 'Empirical Prediction'])
plt.xlim(-0.5, 4.5)
plt.xticks(np.arange(5), ["MNIST", "FMNIST", "C10", "C100", "CARTPOLE"])
plt.ylim(0, 0.5)

plt.show()
