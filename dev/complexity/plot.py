import csv

import numpy as np

from sklearn.svm import SVR, SVC
from sklearn.covariance import ShrunkCovariance
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn import metrics

import matplotlib.pyplot as plt


def area_under_curve(model):
    # Get 100 data points
    x = np.arange(0, 1, 0.001)
    x = np.reshape(x,(-1, 1))

    # Get y prediction 
    y = regressor.predict(x)

    # Do math
    AuC = 0.0
    for ind, val in enumerate(x[1:]):
        y1 = y[ind]
        y2 = y[ind-1]

        if y1 < 0 or y2 < 0:
            continue
        width = 0.01
        square   = width * min(y1, y2) 
        triangle = 0.5 * width * abs(y1 - y2)

        box = square + triangle

        AuC += box

    return AuC

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

        #print(row)
        if row[0] == 'CARTPOLE' and datum[-1] < 0.6:
            continue
        results[row[0]].append(datum)
k = []
fig, axs = plt.subplots(2, 3)
c = 0
for name in results.keys():
    continue
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
    #regressor = SVR(kernel='linear', C=10, gamma=5.0, epsilon=0.1)

    #regressor.fit(x_data, y_data) #training the algorithm

    parameters = {'kernel':['rbf', 'linear', 'poly'], 'C' :[0.0001, 0.01, 10, 100],
                  'gamma': [0.00001,0.1, 10, 100], 'epsilon':[0.00001, 0.1, 10, 100]}
    regressor = GridSearchCV(SVR(), parameters)

    regressor.fit(x_data, y_data)

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

    axs[c % 2, c % 3].scatter(x_data, y_data)
    axs[c % 2, c % 3].scatter(x_data, pred)
    axs[c % 2, c % 3].set_xlabel('Accuracy')
    axs[c % 2, c % 3].set_ylabel('log(TP)')
    axs[c % 2, c % 3].set_title(name)

    point = np.reshape(np.asarray([1.0]), (-1,1))
    k.append(regressor.predict(point)[0])


    print('TP-log-1.0: %.2f'
      % (k[-1]))

    print("AuC:", str(round(area_under_curve(regressor), 4)))

    print('----')
    c = c + 1

plt.show()
s = sum(k)
for ind, val in enumerate(k):
    k[ind] = val/s

    print(round(k[ind],4))

e = [88.0205,
85.1328,
136.8024,
194.6641,
15.1936]

e_s = sum(e)
for ind, val in enumerate(e):
    e[ind] = val/e_s
    print(round(e[ind],4))


e = [182532.4206179811,
211904.015471518,
269661.94757943094,
434866.9281534464,
50090.15641089917]

e_s = sum(e)
for ind, val in enumerate(e):
    e[ind] = val/e_s
    print(round(e[ind],4))

