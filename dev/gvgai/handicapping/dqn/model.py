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


# Load data from data dir
def load_data():
    # Number of files per model
    file_num = 0
    file_counter = 0

    # Get all file paths
    data_path = './data/'
    file_names = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    # Holds data
    data = list()
    results = dict()

    # Open every file
    for file_name in ['data_fix.csv']:
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                # Name, nodes, layers, TP, NTP, score
                if row[0] == 'CARTPOLE':
                    continue

                if row[0] == 'gvgai-missilecommand-lvl0-v0':
                    continue

                datum = list()
                datum.append(int(row[1]))
                datum.append(int(row[2]))
                datum.append(int(row[3]))
                datum.append(float(row[5]))

                if int(row[3]) > 3000000:
                    continue

                # Check if name already exists
                if row[0] not in results:
                    results[row[0]] = []

                results[row[0]].append(datum)

        file_counter = file_counter + 1
        if file_counter >= file_num:
            file_counter = 0
            data.append(results)
            results = dict()


    return data

def main():
    # Get data from data file
    data = load_data()

    a = []
    b = []

    # Go through each inst of data
    for sample in data:
        for key in sample.keys():
            if sample[key][0][2] == 0.0:
                continue

            tmp = np.asarray(sample[key])
            x = tmp[:,2]
            y = np.asarray(tmp[:, 3])
            if min(y) != max(y):
                t = np.divide(np.subtract(y, min(y)), (max(y) - min(y)))
            else:
                t = y

            a = a + x.tolist()
            b = b + t.tolist()

            plt.scatter(x, t, label=key)
    print(a)
    print(b)
    print(len(a))
    r = np.corrcoef(a, b)[0][1]
    r = round(r, 3)
    plt.title('r: ' + str(r) + ', p: ' + str(0.39))
    plt.legend(loc="upper left")
    plt.show()

    return None


if __name__ == "__main__":
    main()
