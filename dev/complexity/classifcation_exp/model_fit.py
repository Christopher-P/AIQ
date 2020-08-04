import csv

import numpy as np

from sklearn.svm import SVR, SVC
from sklearn.covariance import ShrunkCovariance
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn import metrics

import matplotlib.pyplot as plt


def area_under_curve(model, data):
    width_const = 0.001

    # Get 100 data points
    x = np.arange(min(data)[0], max(data)[0], width_const)
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
        width = width_const
        square   = width * min(y1, y2) 
        triangle = 0.5 * width * abs(y1 - y2)

        box = square + triangle

        AuC += box

    # Scale by size
    AuC = AuC / abs(min(data)[0] - max(data)[0])

    return AuC

# Bin data according to mean
def box_data(data):
    number_boxes = 20 + 1
    new_data = dict()

    # Process by names
    for name in data.keys():
        # get score
        x_data = []
        # TP
        y_data = []
        for i in data[name]:
            x_data.append(i[4])
            y_data.append(i[2])
        
        # Find min/max score
        min_s = min(x_data)
        max_s = max(x_data)

        a = np.arange(min_s, max_s, (max_s - min_s)/number_boxes)
        
        for ind, val in enumerate(x_data):
            x_sum = 0
            y_sum = 0
            count = 0
            for ind2, val2 in enumerate(a[0:len(a)-1]):
                if x_data[ind] >= a[ind2] and x_data[ind] < a[ind2+1]:
                    x_sum += x_data[ind]
                    y_sum += y_data[ind]
                    count += 1
            # Check for non zero count
            if count == 0:
                continue

            # Get averages and save it
            x_avg = x_sum / count
            y_avg = y_sum / count

            # Check if it already exists
            if name not in new_data:
                new_data[name] = []

            new_data[name].append([x_avg, y_avg])

    return new_data, std

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

# Bin the data
#results = box_data(results)
#print(results)

k = []
fig, axs = plt.subplots(2, 3)
c = 0
e = []
AuCs = []
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
    #regressor = SVR(kernel='linear', C=10, gamma=5.0, epsilon=0.1)

    #regressor.fit(x_data, y_data) #training the algorithm

    parameters = {'kernel':['rbf', 'linear', 'poly', 'sigmoid'], 'C' :[0.0001, 0.01, 10, 100],
                  'gamma': [0.00001,0.1, 10, 100], 'epsilon':[0.00001, 0.1, 10, 100]}
    regressor = GridSearchCV(SVR(), parameters)

    regressor.fit(x_data, y_data)

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

    e.append(round(area_under_curve(regressor, x_data), 4))
    AuCs.append(e[-1])

    print("AuC:", str(e[-1]))

    print('----')
    c = c + 1

print('AuCs:', AuCs)

plt.show()
s = sum(k)
for ind, val in enumerate(k):
    k[ind] = val/s

    print(round(k[ind],4))



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

import matplotlib.pyplot as plt
import numpy as np

# construct some data like what you have:
x = np.random.randn(100, 5)
mins = x.min(0)
maxes = x.max(0)
means = x.mean(0)
std = x.std(0)

# create stacked errorbars:
plt.errorbar(np.arange(5), means, std, fmt='ok', lw=3)
plt.errorbar(np.arange(5), means, [means - mins, maxes - means],
             fmt='.k', ecolor='gray', lw=1)
plt.xlim(-1, 5)

plt.show()

