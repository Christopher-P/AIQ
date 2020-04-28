import csv
import math
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
import copy

from numpy import prod

def d_t(res):
    # preseve original data
    res_c = copy.deepcopy(res)

    # find order in which to have the algorithm run
    # init conditions
    
    d_max = -10.0
    d_ind = -1
    
    # find first value
    for ind,val in enumerate(res_c):
        if max(val) > d_max:
            d_max = max(val)
            d_ind = ind

    # append index of first value


    # to find next value,  find which test achieves largest max d(t1,t2)
    prev = d_ind
    data = []
    for ind,val in enumerate(res_c):
        res_c[ind] = list(val)

    for i in range(len(res_c)):
        data.append(prev) 
        #remove column
        for ind,val in enumerate(res_c):
            res_c[ind][prev] = -1.0
        # Simple search
        #prev = np.argmax(res_c[prev])
        # cross search
        dr = []
        dr_ind = 1
        dr_max = -10.0
        j_max = -1
        found = False

        for ind, j in enumerate(data): 
            for inn, r in enumerate(res_c[j]):
                if np.max(r) > dr_max:
                    dr_max = np.max(r)
                    dr_ind = np.argmax(r)
                    found = True
            if found:
                j_max = ind

        prev = j_max       
    
    return data

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
            res[keys[val[0]]][keys[val[1]]] = 1.0 - 0.99999
            res[keys[val[1]]][keys[val[0]]] = 1.0 - 0.99999
        elif val[2] == 0.0:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - 0.00001
            res[keys[val[1]]][keys[val[0]]] = 1.0 - 0.00001
        else:
            res[keys[val[0]]][keys[val[1]]] = 1.0 - val[2]
            res[keys[val[1]]][keys[val[0]]] = 1.0 - val[2]


    # normal (with sum)
    # sort to find complex maximal achievment in dissimialrity
    l = d_t(res)
    print(l)

    d_1 = []
    now = 0.0
    next = 0.0
    count = 0.0
    for i in l:
        d_1.append(now/10)
        now = next
        next = next + sum(res[i][0:int(count+1)]) / (count + 1)
        count = count + 1
    d_1.append(now/10)
    d_1.append(next/10)

    # min
    # sort to find simple maximal achievment in dissimialrity
    d_2 = []
    now = 0.0
    next = 0.0
    count = 0.0
    for i in l:
        d_2.append(now)
        now = next
        next = next +  min(res[i][0:int(count+1)]) / (count + 1)
        count = count + 1
    d_2.append(now)
    d_2.append(next)
    # product
    # sort to find simple maximal achievment in dissimialrity
    d_3 = []
    now = 0.0
    next = 0.0
    count = 0.0
    for i in l:
        d_3.append(now)
        now = next
        next = next + prod(res[i][0:int(count+1)]) / (count + 1)
        count = count + 1
    d_3.append(now)
    d_3.append(next)


    print(d_1)
    print(d_2)
    print(d_3)

    y = range(len(d_1))
    plt.plot(y, d_1, y, d_2, y, d_3)
    plt.legend(['SUM/10','MIN','PRODUCT'])
    plt.title('Complex')
    plt.ylabel('Diversity')
    plt.xlabel('# of tests')
    plt.xticks([0,1] + list(range(2, len(y))), [0,0] + list(range(1, len(y))))
    # Label points
    names = list(keys.keys())
    for i, txt in enumerate(l):
        plt.annotate(names[txt], (y[2:][i],d_1[2:][i]), rotation=25)
    names = list(keys.keys())
    for i, txt in enumerate(l):
        plt.annotate(names[txt], (y[2:][i],d_2[2:][i]), rotation=35)
    names = list(keys.keys())
    for i, txt in enumerate(l):
        plt.annotate(names[txt], (y[2:][i],d_3[2:][i]), rotation=45, ma='center')


    plt.show()


    with open('nice results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        fieldnames = list(keys.keys())
        spamwriter.writerow(fieldnames)
        for ind, val in enumerate(res):
            name = list(keys.keys())[ind]
            spamwriter.writerow([name, *val])

        

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
cross_table(info)

