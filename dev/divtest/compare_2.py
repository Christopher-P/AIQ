import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import copy

from numpy import prod

## Holder function
def holder_aiq(ID_partial, ID_full, scores):
    # Find normalization factor for set diverseity
    # D = 1 for all tests included.
    nfac = len(ID_full)/sum(ID_full)
    
    # Find set diversity
    D = sum(ID_partial)/len(ID_full)

    # Calculate aiq score according to formula
    aiq = D * nfac * sum(scores)
    #print("E", D * nfac)
    return D * nfac

## Chris function
def chris_aiq(ID_partial, ID_full, scores):
    # ID is not summ normalized, fix
    ID_partial = ID_partial / sum(ID_full)

    # Multiply by n
    ID_partial = ID_partial 

    aiq = 0.0
    
    for ind,val in enumerate(ID_partial):
        aiq += ID_partial[ind] * scores[ind]

    return sum(ID_partial)

def cross_table(data, scores):
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
            res[keys[val[0]]][keys[val[1]]] = 1.0 - 0.9999
            res[keys[val[1]]][keys[val[0]]] = 1.0 - 0.9999
        elif val[2] == 0.0:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - 0.0001
            res[keys[val[1]]][keys[val[0]]] = 1.0 - 0.0001
        else:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - val[2]
            res[keys[val[1]]][keys[val[0]]] = 1.0 - val[2]


    ### Find individual diversity
    
    # ID = (A + B + C + ... + Z) / N
    ID = []
    for i in res:
        ID.append(sum(i)/len(i))

    # Get full aiq scores
    h1 = holder_aiq(ID,ID,scores)
    c1 = chris_aiq(ID,ID,scores)

    # Get diverse set
    # Hard Coded set
    di,d = zip(*(reversed(sorted(zip(ID, scores)))))
    ID = list(di)
    scores = list(d)
    a = 0
    b = 5
    h2 = holder_aiq(ID[0:5],ID,scores[0:5])
    c2 = chris_aiq(ID[0:5],ID,scores[0:5])

    # Get similar set
    h3 = holder_aiq(ID[7:11],ID,scores[7:11])
    c3 = chris_aiq(ID[7:11],ID,scores[7:11])

    # Get single set
    h4 = holder_aiq([ID[6]],ID,[scores[6]])
    c4 = chris_aiq([ID[6]],ID,[scores[6]])

    print(h1,c1)
    print(h2,c2)
    print(h3,c3)
    print(h4,c4)

    plotit((h1,h2,h3,h4),(c1,c2,c3,c4))

def plotit(d1, d2):
    n_groups = len(d1)
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, d1, bar_width,
    alpha=opacity,
    color='b',
    label='D')

    rects2 = plt.bar(index + bar_width, d2, bar_width,
    alpha=opacity,
    color='g',
    label='sum(ID)')

    plt.xlabel('Different Sets')
    plt.ylabel("Diversity \'multiplier\'")
    plt.title('Different multipliers compared by sets')
    plt.xticks(index + bar_width, ('All', 'Top 4 Diverse', 'Bot 4 diverse', 'One average test'), rotation=15)
    plt.legend()

    plt.savefig('D_Mulitiplier_methods.png',dpi=200)
    plt.tight_layout()
    plt.show()



### Import and process raw data
data = []

with open('raw_data.csv', newline='') as csvfile:
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

# Holds the score from each test that is same (A = B)
scores = []

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
        
        names = str(val[0]).split('=')
        if names[0] == names[1]:
            vals = [float(i) for i in val[5:25]]
            if max(vals) == min(vals):
                s = 0.0
            else:
                s = (float(val[2]) - min(vals)) / (max(vals) - min(vals))
            scores.append(s)

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

cross_table(info, scores)
