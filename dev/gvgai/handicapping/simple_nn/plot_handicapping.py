import csv

import numpy as np

from statistics import variance, mean, stdev
import copy

import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


# Load data from data dir
def load_data():
    # Get all file paths
    data_path = './data/'
    file_names = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    # Holds data
    results = dict()

    # Open every file
    for file_name in file_names:
        with open(data_path + file_name, newline='') as csvfile:
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

                results[row[0]].append(datum)

    return results


def main():
    data = load_data()
    print(data)

    invalid_tests = ['gvgai-boulderdash-lvl0-v0', 'gvgai-chase-lvl0-v0', 'gvgai-missilecommand-lvl0-v0']
    x_avg = []
    y_avg = []

    for test_name in data:
        if test_name in invalid_tests:
            continue
        else:
            # Grab data from array
            working = np.array(data[test_name])
            scores = working[:, 4]
            tp = working[:, 2]

            # Normalize score
            scores = (scores - np.min(scores))/np.ptp(scores)

            # Sort (for plotting line part)
            tp, scores = zip(*sorted(zip(tp, scores)))

            # Plot data
            plt.scatter(tp, scores, label=test_name)
            plt.plot(tp, scores)

            # Append data for trendline
            x_avg = x_avg + list(tp)
            y_avg = y_avg + list(scores)

    z = np.polyfit(x_avg, y_avg, 1)
    p = np.poly1d(z)
    plt.plot(x_avg, p(x_avg), "--", color='black', label='Linear Trend')

    plt.ylabel('Normalized Score [0,1]')
    plt.xlabel('Trainable Parameters')
    plt.legend()
    plt.show()



    # Display full plot

if __name__ == "__main__":
    main()
