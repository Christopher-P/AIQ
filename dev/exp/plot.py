### Used to plot experimental results from run.py
import csv
import numpy as np

import matplotlib.pyplot as plt

def load_file(filename):
    data = []
    with open('data/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        for row in spamreader:
            data.append((row[0], row[1], row[2]))

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
    #res[5,7] = res[7,5]
    #res[7,5] = 0.0

    # See what data is missing (maximize everything)
    for ind,val in enumerate(res):
        for ind2,val2 in enumerate(val):
            if ind2 < ind:
                continue
            if val2 == 0.0:
                print(list(keys.keys())[ind],list(keys.keys())[ind2])

    ### NEW CODE
    ## Fill out table (remove 0.0 values)
    #for i in range(10):
    #    for j in range(10):
    #        res[j,i] = res[i,j]
                

    plt.imshow(res, cmap='hot', interpolation='nearest')
    plt.show()

    # new plot
    fig, ax = plt.subplots(figsize=(14, 10))
    im = ax.imshow(res)

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


data = load_file('Reward.csv')
cross_table(data)
