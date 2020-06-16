import csv

import numpy as np

from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn import metrics

import matplotlib.pyplot as plt

with open('data/results.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    # Name, nodes, layers, TP, NTP, score
    results = dict()
    for row in spamreader:
        datum  = []
        datum.append(int(row[1]))
        datum.append(int(row[2]))
        datum.append(int(row[3]))
        datum.append(int(row[4]))
        datum.append(float(row[5]))
        
        # Check if it already exists
        if row[0] not in results:
            results[row[0]] = []

        print(row)
        results[row[0]].append(datum)
k = []
for name in results.keys():
    # get TP
    x_data = []
    # SCORE
    y_data = []
    for i in results[name]:
        x_data.append(i[4])
        y_data.append(i[2])

    # Reshape because we have one feature
    x_data = np.reshape(np.asarray(x_data),(-1, 1))   

    # Log the y_data (its too big
    y_data = np.log(y_data)
    
    # Linear regression
    # Ax + B
    regressor = SVR(kernel='linear', C=10, gamma=5.0, epsilon=0.1)

    regressor.fit(x_data, y_data) #training the algorithm

    #To retrieve the intercept:
    #print(regressor.intercept_)
    #For retrieving the slope:
    #print(regressor.coef_)

    pred = regressor.predict(x_data)

    print('Name: {0}'.format(name))

    print('Mean squared error: %.2f'
      % metrics.mean_squared_error(y_data, pred))

    print('Coefficient of determination: %.2f'
      % metrics.r2_score(y_data, pred))

    #print(x_data, y_data)

    plt.scatter(x_data, y_data)
    plt.scatter(x_data, pred)
    plt.show()

    point = np.reshape(np.asarray([1.0]), (-1,1))
    k.append(regressor.predict(point)[0])


    print('TP-log-0.95: %.2f'
      % (k[-1]))

    print('----')

s = sum(k)
for ind, val in enumerate(k):
    k[ind] = val/s

    print(round(k[ind],4))

e = [16436.015873511333,
45807.61072698963,
103565.54283482285,
102674.11866437038,
90.15641091228197]

e_s = sum(e)
for ind, val in enumerate(e):
    e[ind] = val/e_s
    print(round(e[ind],4))

