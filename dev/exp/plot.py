### Used to plot experimental results from run.py

import csv

def load_file(filename):
    name_A = []
    name_B = []
    score  = []
    with open('data/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        for row in spamreader:
            name_A.append(row[0])
            name_B.append(row[1])
            score.append(row[2])

    return name_A, name_B, score



a,b,c = load_file('Reward.csv')

