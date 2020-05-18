from os import listdir
from os.path import isfile, join

import csv

import numpy as np
import matplotlib.pyplot as plt

def load_data(data_path, skip):
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    all_data = []
    for name in onlyfiles:
        data = load_file(data_path + name, skip)
        if data is None:
            continue
        else:
            all_data.append(data)

    return all_data


def load_file(filename, skip):
    data_all = []
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            data = []
            data.append(str(row[0]))    # Name 1
            data.append(str(row[1]))    # Name 2
            data.append(int(row[2]))    # Nodes
            data.append(int(row[3]))    # Layers
            data.append(int(row[4]))    # TP
            data.append(int(row[5]))    # NTP
            data.append(float(row[6]))  # p 
            data.append(float(row[7]))  # A
            data.append(float(row[8]))  # B 
            data.append(float(row[9]))  # AB 

            if data[1] == skip:
                return None

            data_all.append(data)

    return data_all

# Return x_arr = tp, y_arr = sim 
def sim_measure(data):
    x_arr = []
    y_arr = []
    w = []
    z = []
    
    for exp in data:
        s_sum = 0.0
        s_list = []

        for i in exp:
            a = max(i[7], i[8])
            b = min(i[7], i[8])
            ab = i[9] 
            
            if ab > a or ab < b:
                a = 0
                s_sum = s_sum + 1.0
                s_list.append(1.0)
            else:
            
                try:
                    s_sum = s_sum + abs(abs(a - ab) - abs(b - ab))/abs(a - b)
                    s_list.append(abs(abs(a - ab) - abs(b - ab))/abs(a - b))
                except:
                    print('div 0')

        #if s_sum / len(s_list) > 0.7:
        #    continue

        # Append sim
        y_arr.append(s_sum / len(s_list))
        # Append TP
        x_arr.append(exp[0][4])
        # Append layers
        w.append(exp[0][3])
        # Append nodes
        z.append(exp[0][2])

    return x_arr, y_arr, w, z

def plot(x, y, x_labels, names):
    for ind, val in enumerate(x):
        # Figure formatting
        plt.subplot(231 +ind)
        coef = np.polyfit(x[ind], y[ind], 1)
        poly1d_fn = np.poly1d(coef) 
        # poly1d_fn is now a function which takes in x and returns an estimate for y
        p = np.corrcoef(x[ind], y[ind])[0, 1]
        p = round(p, 3)

        plt.plot(x[ind], y[ind], 'ro', x[ind], poly1d_fn(x[ind]), '--k')
        plt.xlabel(x_labels[ind])
        plt.ylabel('Similarity')
        plt.title(names[ind] + ', p=' + str(p))

    plt.show()
    
# Mnist to Fmnist
data_path = 'data_1/'
data = load_data(data_path, skip='MNIST')

# Mnist to mnist
data_path = 'data_2/'
data2 = load_data(data_path, skip='')

# y = sim,  x = tp, w = layers, z = nodes
diff_x, diff_y, diff_w, diff_z = sim_measure(data)
same_x, same_y, same_w, same_z = sim_measure(data2)

x_dats = [diff_x, diff_w, diff_z, same_x, same_w, same_z]
y_dats = [same_y, same_y, same_y, diff_y, diff_y, diff_y]

x_labels = ['TP', 'Layers', 'Nodes','TP', 'Layers', 'Nodes']
names    = ['Mnist vs Mnist'] * 3 + ['Mnist vs Fmnist'] * 3 

plot(x_dats, y_dats, x_labels,names)


