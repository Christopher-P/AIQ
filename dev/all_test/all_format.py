import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

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

    for val in data:
        res[keys[val[0]]][keys[val[1]]] = val[2]

    print(res)

    with open('nice results 1000.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        fieldnames = list(keys.keys())
        spamwriter.writerow(fieldnames)
        for ind, val in enumerate(res):
            name = list(keys.keys())[ind]
            spamwriter.writerow([name, *val])

        flat_list = [item for sublist in res for item in sublist]
        avg = 0.0
        cnt = 0.0
        for i in flat_list:
            if i == 0.0:
                continue   
            else:
                avg += i
                cnt += 1
        avg = avg/cnt

        spamwriter.writerow(('AVERAGE', avg))

    plt.imshow(res, cmap='hot', interpolation='nearest')
    plt.savefig('1000.png')
    plt.show()

    return None


data = []

with open('all_test_data-1000.csv', newline='') as csvfile:
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
    if ind < 20:
        continue

    # looks like --> 0=10
    name = str(val[0]).split('=')
    
    # get a, b baselines
    A = float(data[int(name[0])][2])
    B = float(data[int(name[1])][2])

    # find min/max
    Vmax = max(A,B)
    Vmin = min(A,B)
       
    # get mixed values
    V = float(val[2])
    if A == B:
        S = 0
    else:
        S = abs(abs(Vmax - V) - abs(Vmin - V) ) / abs( A  - B )
    info.append((name[0], name[1], S))         


    counter += 1
    continue

cross_table(info)

