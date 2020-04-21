import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import copy

from numpy import prod
import random

## Holder function
def holder_aiq(ID_partial, ID_full, scores):
    # Find normalization factor for set diverseity
    # D = 1 for all tests included.
    nfac = len(ID_full)/sum(ID_full)
    
    # Find set diversity
    D = sum(ID_partial)/len(ID_full)

    # Calculate aiq score according to formula
    aiq = D * nfac * sum(scores)
    return aiq / len(ID_full)

## Chris function
def chris_aiq(ID_partial, ID_full, scores):
    # ID is not summ normalized, fix
    ID_partial = ID_partial / sum(ID_full)

    # Multiply by n
    ID_partial = ID_partial * len(ID_partial)

    aiq = 0.0
    
    for ind,val in enumerate(ID_partial):
        aiq += ID_partial[ind] * scores[ind]

    return aiq / len(ID_full)

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
    nam = list(keys.keys())
    di,d,nam2 = zip(*(reversed(sorted(zip(ID, scores,nam)))))
    ID = list(di)
    scores = list(d)
    nam = list(nam2)
    a = 0
    b = 5
    h2 = holder_aiq(ID[0:5],ID,scores[0:5])
    c2 = chris_aiq(ID[0:5],ID,scores[0:5])

    # Get similar set
    h3 = holder_aiq(ID[7:11],ID,scores[7:11])
    c3 = chris_aiq(ID[7:11],ID,scores[7:11])

    for ind, val in enumerate(ID):
        print('{:20s}'.format(nam[ind]), "{0:.2f}".format(scores[ind]), "{0:.2f}".format(ID[ind]))

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
    label='D * sum(S*C)')

    rects2 = plt.bar(index + bar_width, d2, bar_width,
    alpha=opacity,
    color='g',
    label='sum(D*S*C)')

    plt.xlabel('Different Sets')
    plt.ylabel('AIQ')
    plt.title('Different sets compared by methods (C = 1)')
    plt.xticks(index + bar_width, ('All', 'Top 4 Diverse', 'Bot 4 diverse', 'One average test'), rotation=15)
    plt.legend()

    plt.savefig('D_methods.png',dpi=200)
    plt.tight_layout()
    plt.show()

def load_data():
    first = True
    name_vals = dict()
    val_names = dict()
    data = []
    tabled = []
    with open('nice_results.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if first:
                first = not first
                c = 0
                for element in row:
                    name_vals[element] = c
                    name_vals[c] = element
                    c = c + 1
                continue
            
            d = []
            for element in row[1:]:
                d.append(element)
            data.append(d)

    for i in range(len(data)):
        for j in range(len(data)):
            tabled.append((name_vals[i], name_vals[j], float(data[i][j])))

    #print(name_vals)
    #print(data)
    #print(tabled)
    #exit()
    return tabled


info = load_data()

# Scores is a list of scores for same name pairings
scores = []
random.seed(1243)
for i in range(10):
    scores.append(random.random())
print(scores)
cross_table(info, scores)



