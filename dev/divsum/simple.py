import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import copy

from numpy import prod

def d_t(res):

    return None

def cross_table(data):
    counter = 0
    keys = {}
    for val in data:
        if val[0] not in keys:
            keys[val[0]] = counter
            counter += 1
        if val[1] not in keys:
            keys[val[1]] = counter
            counter += 1

    res = np.zeros([len(keys),len(keys)])

    # 1 - x because we want dissimilarity
    for val in data:
        if val[2] == 1.0:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - 0.99
            res[keys[val[1]]][keys[val[0]]] = 1.0 - 0.99
        elif val[2] == 0.0:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - 0.01
            res[keys[val[1]]][keys[val[0]]] = 1.0 - 0.01
        else:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - val[2]
            res[keys[val[1]]][keys[val[0]]] = 1.0 - val[2]


    # normal (with sum)
    # sort to find simple maximal achievment in dissimialrity
    d = []
    for i in res:
        d.append(max(i))

    # get indices of array max values
    l_1 = np.argsort(d)
    # returns least to most, reverse array
    l_1 = l_1[::-1]

    d_1 = []
    now = 0.0
    next = 0.0
    count = 0.0
    for i in l_1:
        d_1.append(now/10)
        now = next
        next = next + sum(res[i]) / (count + 1)
        count = count + 1
    d_1.append(now/10)
    d_1.append(next/10)

    # min
    # sort to find simple maximal achievment in dissimialrity
    d = []
    for i in res:
        d.append(min(i))

    # get indices of array max values
    l_2 = np.argsort(d)
    # returns least to most, reverse array
    l_2 = l_2[::-1]

    d_2 = []
    now = 0.0
    next = 0.0
    count = 0.0
    for i in l_2:
        d_2.append(now)
        now = next
        next = next +  min(res[i]) / (count + 1)
        count = count + 1
    d_2.append(now)
    d_2.append(next)
    # product
    # sort to find simple maximal achievment in dissimialrity
    d = []
    for i in res:
        d.append(prod(i))

    # get indices of array max values
    l_3 = np.argsort(d)
    # returns least to most, reverse array
    l_3 = l_3[::-1]
    d_3 = []
    now = 0.0
    next = 0.0
    count = 0.0
    for i in l_3:
        d_3.append(now)
        now = next
        next = next + prod(res[i]) / (count + 1)
        count = count + 1
    d_3.append(now)
    d_3.append(next)

    print(d_1)
    print(d_2)
    print(d_3)

    y = range(len(d_1))
    plt.plot(y, d_1, y, d_2, y, d_3)
    plt.legend(['SUM/10','MIN','PRODUCT'])
    plt.title('Simple Search ')
    plt.ylabel('Diversity')
    plt.xlabel('# of tests')
    plt.xticks([0,1] + list(range(2, len(y))), [0,0] + list(range(1, len(y))))
    # Label points
    names = list(keys.keys())
    for i, txt in enumerate(l_1):
        plt.annotate(names[txt], (y[2:][i],d_1[2:][i]), rotation=25)
    names = list(keys.keys())
    for i, txt in enumerate(l_2):
        plt.annotate(names[txt], (y[2:][i],d_2[2:][i]), rotation=35)
    names = list(keys.keys())
    for i, txt in enumerate(l_3):
        plt.annotate(names[txt], (y[2:][i],d_3[2:][i]), rotation=45, ma='center')


    plt.show()


    with open('nice results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        fieldnames = list(keys.keys())
        spamwriter.writerow(fieldnames)
        for ind, val in enumerate(res):
            name = list(keys.keys())[ind]
            spamwriter.writerow([name, *val])

        



data = []

with open('d=1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

#print(data)

A = None
B = None
name1 = None
name2 = None
counter = 0
info = []

for ind, val in enumerate(data):
    if counter >= 3:
        counter = 0
    
    if counter == 0:
        name1 = val[0]
        A = float(val[2])

    elif counter == 1:
        name2 = val[0]
        B = float(val[2])

    elif counter == 2:
        Vmax = max(A,B)
        Vmin = min(A,B)
        V = float(val[2])
        if A == B:
            S = 0.5
        else:
            S = abs(abs(Vmax - V) - abs(Vmin - V) ) / abs( A  - B )
        info.append((name1, name2, S))         

    else:
        print('error')
        exit()

    counter += 1
    continue

cross_table(info)

