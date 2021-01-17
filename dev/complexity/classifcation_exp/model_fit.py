import csv

import numpy as np

from sklearn.svm import SVR, SVC
from sklearn.covariance import ShrunkCovariance
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn import metrics

from statistics import variance, mean, stdev
import copy

import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


def area_under_curve(model, data):
    width_const = 0.0001

    # Get 100 data points
    x = np.arange(0, 1, width_const)
    x = np.reshape(x, (-1, 1))

    # Get y prediction 
    y = model.predict(x)

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
    #AuC = AuC / (abs(min(data) - max(data)))
    #AuC = AuC / min(data)
    #print(variance(data))
    #AuC = AuC / (mean(data) * variance(data))

    return AuC


# Load data from data dir
def load_data():
    # Number of files per model
    file_num = 1
    file_counter = 0

    # Get all file paths
    data_path = './data_2/'
    file_names = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    # Holds data
    data = list()
    results = dict()

    # Open every file
    for file_name in file_names:
        #with open(data_path + file_name, newline='') as csvfile:
        with open('prelim_results.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                # Name, nodes, layers, TP, NTP, score
                datum = list()
                datum.append(int(row[1]))
                datum.append(int(row[2]))
                datum.append(int(row[3]))
                datum.append(int(row[4]))
                datum.append(float(row[5]))

                # Check if name already exists
                if row[0] not in results:
                    results[row[0]] = []

                '''
                # Remove outliers (about random)
                if row[0] == "C100":
                    if datum[4] < 0.02:
                        continue
                else:
                    if datum[4] < 0.15:
                        continue
                '''

                results[row[0]].append(datum)

        file_counter = file_counter + 1
        if file_counter >= file_num:
            file_counter = 0
            data.append(results)
            results = dict()

        break
    #data.append(results)

    return data


# Create a model to fit the data
def create_model(name, data_sample):
    # Use Score here
    x_data = []
    # Use Trainable Parameters here
    y_data = []

    for i in data_sample:
        x_data.append(i[4])
        y_data.append(i[2])

    # Data copy
    x_data_nominal = copy.deepcopy(x_data)

    # Reshape because we have one feature
    x_data = np.reshape(np.asarray(x_data), (-1, 1))

    # Log the y_data (its too big)
    y_data = np.log(y_data)

    # Do some hyper param searching here
    parameters = {'kernel':['rbf', 'linear', 'poly'], 'C' :[0.0001, 0.01, 10, 100],
                  'gamma': [0.00001,0.1, 10, 100], 'epsilon':[0.00001, 0.1, 10, 100]}
    regressor = GridSearchCV(SVR(), parameters)

    # Fit model
    regressor.fit(x_data, y_data)

    # Check accuracy of trained on data
    pred = regressor.predict(x_data)

    print('Name: {0}'.format(name))

    print('Mean squared error: %.2f'
          % metrics.mean_squared_error(y_data, pred))

    print('Coefficient of determination: %.2f'
          % metrics.r2_score(y_data, pred))

    area_under = round(area_under_curve(regressor, x_data_nominal), 4)

    print("AuC:", str(area_under))

    print('----')

    plt.scatter(x_data, y_data)
    plt.scatter(x_data, pred)
    plt.show()

    return area_under


# Store AuC and name to csv for plotting
def log_results(name, AuC):
    with open('results_model_fit.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow((name, AuC))
    return None


def main():
    # Get data from data file
    data = load_data()

    # Go through each inst of data
    for sample in data:
        for key in sample.keys():
            AuC = create_model(key, sample[key])
            log_results(key, AuC)

    return None

'''
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
e = []
AuCs = []

random_mins = {"MNIST":0.1, "FMNIST":0.1, "C10":0.1, "C100":0.01, "CARTPOLE":0.5}

for name in results.keys():
    # Get random min values
    ran_min = random_mins[name]

    # get TP
    x_data = []
    # SCORE
    y_data = []

    for i in results[name]:
        x_data.append(i[4])
        y_data.append(i[2])

    x_data_nominal = copy.deepcopy(x_data)

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

    e.append(round(area_under_curve(regressor, x_data_nominal, ran_min), 4))
    AuCs.append(e[-1])

    print("AuC:", str(e[-1]))

    print('----')
    c = c + 1

print('AuCs:', AuCs)

#plt.show()
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
'''

if __name__ == "__main__":
    main()
