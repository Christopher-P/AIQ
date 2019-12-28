import csv

with open('data/RAW.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
    for row in spamreader:
        print(row[0], row[1])



