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
    file_num = 1
    file_counter = 0

    # Get all file paths
    #data_path = './data/'
    #file_names = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    # Holds data
    data = list()
    results = dict()

    # Open every file
    tp = -1000

    with open('data_fix.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # Name, nodes, layers, TP, NTP, score
            if row[0] == 'CARTPOLE':
                continue

            datum = list()
            datum.append(int(row[1]))
            datum.append(int(row[2]))
            datum.append(int(row[3]))
            datum.append(int(row[4]))
            l = int(row[5])
            r = row[6:l+6]
            n = row[6+l:]
            datum.append(list(map(float, r)))
            datum.append(list(map(float, n)))

            data.append(datum)

            if datum[2] > tp:
                tp = datum[2]

    return data, tp

def main():
    # Get data from data file
    data, max_tp = load_data()

    axes = plt.gca()
    axes.set_xlim([0, 500000])
    #axes.set_ylim([ymin, ymax])

    # Go through each inst of data
    for sample in data:
        x = np.asarray(sample[5])
        y = np.asarray(sample[4])

        z = np.polyfit(x, y, 10)
        p = np.poly1d(z)
        print('---')
        print(z)
        plt.plot(x, p(x), "b--", label=sample[2], linewidth=sample[2]/max_tp*2.0)
        #plt.plot(x, y, label=sample[2])

    #plt.legend(loc="upper left")
    plt.xlabel('training instances')
    plt.ylabel('score')
    plt.title('Score vs Time, size=TP')
    plt.show()

    return None


if __name__ == "__main__":
    main()
