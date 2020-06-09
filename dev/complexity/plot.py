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

        results[row[0]].append(datum)

for name in results.keys():
    # get TP
    x_data = []
    # SCORE
    y_data = []
    for i in results[name]:
        x_data.append(i[2])
        y_data.append(i[4])

    # Reshape because we have one feature
    x_data = np.reshape(np.asarray(x_data),(-1, 1))   
    
    # Linear regression
    # Ax + B
    regressor = LinearRegression()

    regressor.fit(x_data, y_data) #training the algorithm

    print(name)
    #To retrieve the intercept:
    #print(regressor.intercept_)
    #For retrieving the slope:
    #print(regressor.coef_)

    pred = regressor.predict(x_data)
    #print(pred, y_data)

    print('Mean squared error: %.2f'
      % metrics.mean_squared_error(y_data, pred))

    print('Coefficient of determination: %.2f'
      % metrics.r2_score(y_data, pred))

    print(x_data, y_data)

    plt.plot(x_data, y_data, '-r', x_data, pred, '-b')
    plt.show()



