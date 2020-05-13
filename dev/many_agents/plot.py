import csv
from os import listdir
from os.path import isfile, join


def load_data(data_path):
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    all_data = []
    for name in onlyfiles:
        data = load_file(data_path + name)
        all_data.append(data)

    return all_data


def load_file(filename):
    data_all = []
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            data = []
            data.append(str(row[0]))    # Name 1
            data.append(str(row[1]))    # Name 2
            data.append(int(row[2]))    # Nodes
            data.append(int(row[3]))    # Layers
            data.append(int(row[4]))    # TP
            data.append(int(row[5]))    # NTP
            data.append(float(row[6]))  # p 
            data.append(float(row[6]))  # A
            data.append(float(row[6]))  # B 
            data.append(float(row[6]))  # AB 

            data_all.append(data)

    return data_all


def sim_measure():

    

data_path = 'data/'

data = load_data(data_path)
print(data)
print(data[0])
print(data[0][0])        
