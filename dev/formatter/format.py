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

    with open('nice results.csv', 'w', newline='') as csvfile:
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

    # this one entry is out of whach
    res[5,7] = res[7,5]
    res[7,5] = 0.0

    # See what data is missing (maximize everything)
    for ind,val in enumerate(res):
        for ind2,val2 in enumerate(val):
            if ind2 < ind:
                continue
            if val2 == 0.0:
                print(list(keys.keys())[ind],list(keys.keys())[ind2])

    ### NEW CODE
    ## Fill out table (remove 0.0 values)
    for i in range(10):
        for j in range(10):
            res[j,i] = res[i,j]
                

    #plt.imshow(res, cmap='hot', interpolation='nearest')
    #plt.show()

    # new plot
    fig, ax = plt.subplots(figsize=(14, 10))
    im = ax.imshow(res)
    fig.colorbar(im, orientation='vertical')

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(res)))
    ax.set_yticks(np.arange(len(res)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(list(keys.keys()))
    ax.set_yticklabels(list(keys.keys()))

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")




    # Loop over data dimensions and create text annotations.
    for i in range(len(res)):
        for j in range(len(res)):
            text = ax.text(j, i, round(res[i, j],2), size=13,
                           ha="center", va="center", color="w")

    ax.set_title("Similarity table for current test suite")
    
    fig.tight_layout()
    
    plt.savefig('HeatMap.png', dpi=400)
    plt.show()

    return None


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

