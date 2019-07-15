import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import copy

from numpy import prod
from scipy.optimize import curve_fit

def d_t(res):

    return None

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

def cross_table(data):
    print(data)
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
        res[keys[val[0]]][keys[val[1]]] = 1.0 - val[2]
        res[keys[val[1]]][keys[val[0]]] = 1.0 - val[2]

    # get name list
    names = list(keys.keys())

    # get ID list
    ID = []
    print(res)
    for i in res:
        #print(i)
        ID.append(np.mean(i))

    n = [x for _,x in sorted(zip(ID,names))]
    ID = sorted(ID)

    y_pos = np.arange(len(n))


    plt.bar(y_pos, ID, align='center', alpha=0.5)
    plt.xticks(y_pos, n,rotation=45)
    plt.ylabel('Individual Diversity')
    plt.title('F_Individual Diversities')
    plt.tight_layout()
    plt.savefig('F_Individual_Diversities.png')
    plt.show()

    ### Part 2: get Set ID

    # reverse names and IDs
    names = n[::-1]
    ID = ID[::-1]

    # get norm values
    normed = sum(ID)

    norm_ID = []
    prev = 0.0
    print(ID)
    for i in ID:
        norm_ID.append((i + prev)/normed)
        prev = i + prev

    print(norm_ID)

    popt, pcov = curve_fit(func, y_pos, norm_ID)
    print(popt,pcov)

    plt.plot(y_pos, norm_ID, label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.xticks(y_pos, names,rotation=45)
    plt.ylabel('Set Diversity')
    plt.title('F_Individual Diversities')
    plt.legend()
    plt.tight_layout()
    plt.savefig('F_Set_Diversity.png')
    plt.show()

    exit() 

    with open('nice results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        fieldnames = list(keys.keys())
        spamwriter.writerow(fieldnames)
        for ind, val in enumerate(res):
            name = list(keys.keys())[ind]
            spamwriter.writerow([name, *val])

        



data = []

with open('fake.csv', newline='') as csvfile:
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

