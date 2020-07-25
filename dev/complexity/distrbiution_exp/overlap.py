# Find % overlap of blobs used in main
import random
import numpy as np

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.covariance import EmpiricalCovariance

from statistics import stdev

def gen_data(dist):
    # Dist ranges [0,1]
    dist = dist / 2.0
    n_samples = 50000
    n_bins = 2
    n_features = 10

    centers = [list(np.random.uniform(low=0.5+dist, high=0.5+dist, size=n_features)),
               list(np.random.uniform(low=0.5-dist, high=0.5-dist, size=n_features))]
    X, y = make_blobs(n_samples=n_samples, centers=centers, n_features=n_features, shuffle=False)

    # split train, test for calibration

    # Correct the shape
    #X = np.reshape(X, (len(X), 1, n_features))

    # Conv to one-hot
    #y_train = to_categorical(y_train, n_bins)
    #y_test = to_categorical(y_test, n_bins)

    return X, y, centers

# needs python3.8
def dists(a,b):
    from statistics import stdev, mean, NormalDist
    total = 0.0

    for k in range(10):
        mu_a = mean(a[0][:,k])
        std_a = stdev(a[0][:,k])

        mu_b = mean(b[0][:,k])
        std_b = stdev(b[0][:,k])

        r = NormalDist(mu=mu_a, sigma=std_a).overlap(NormalDist(mu=mu_b, sigma=std_b))
        if total == 0.0:
            total = r
        else:
            total = total * r

    return round(total, 4)

# 20 -> 6 cause first 6 have way tooo much variance
points = 20

# Samples per point
samples = 1

# Stdev ~0.7 dist
std = 6.5

for i in range(samples):
    totals = []
    for j in range(0,points):
        # Generate data / package it
        X, y, centers = gen_data(j/points)

        a = [X[:24999], y[:24999]]
        b = [X[25000:], y[25000:]]

        # do dists:
        total = dists(a,b)
        totals.append(total)
        continue

        # Do montecarlo
        a_a = 0
        a_b = 0
        b_b = 0
        b_a = 0

        # Samples in "a" are belong to center 0
        for samp in a[0]:
            '''            
            # Distance to correct center
            dist_a = np.linalg.norm(samp-centers[0]) 
            # Distance to incorrect center
            dist_b = np.linalg.norm(samp-centers[1]) 

            if std > dist_a and std > dist_b:   
                uni = uni + 1
            else:
                other = other + 1
            '''
            
            # Distance to correct center
            dist_a = np.linalg.norm(samp-centers[0]) 
            # Distance to incorrect center
            dist_b = np.linalg.norm(samp-centers[1]) 
            
            if dist_a < dist_b:
                a_a += 1
            else:
                a_b += 1
            

        # Samples in "b" are belong to center 1
        for samp in b[0]:
            '''
            # Distance to correct center
            dist_a = np.linalg.norm(samp-centers[0]) 
            # Distance to incorrect center
            dist_b = np.linalg.norm(samp-centers[1]) 

            if std > dist_a and std > dist_b:    
                uni = uni + 1
            else:
                other = other + 1
            '''
            # Distance to correct center
            dist_a = np.linalg.norm(samp-centers[0]) 
            # Distance to incorrect center
            dist_b = np.linalg.norm(samp-centers[1]) 
            
            if dist_b < dist_a:
                b_b += 1
            else:
                b_a += 1

        over = round((a_b + b_a) / (a_a + b_b + a_b + b_a),4)
        print(over)
        totals.append(over)
    print(totals)

