import csv

from os import listdir
from os.path import isfile, join

import numpy as np

def load_data():
    # Main data holder
    data = dict()
    
    # Find all files in dir
    mypath = 'data/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # Iterate through all files
    for file_name in onlyfiles:
        
        # Read csv file
        with open(mypath + file_name, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # Row by row
            for row in csv_reader:

                # Check if data exists in data
                if row[0] not in data:
                    data[row[0]] = []
                
                # Add data to dict
                data[row[0]].append(row)
                

    return data


def conform_data(data):
    # Get list of keys
    key_list = data.keys()

    # Get keys for A,B data
    individual = dict()
    for key in key_list:
        if '=' in key:
            continue
        
        # Get individual A data
        sum_score = 0
        for element in data[key]:
            score = element[3]
            sum_score += float(score)

        avg_score = sum_score/len(data[key])

        individual[key] = avg_score

    # Get keys for AB data
    combined = dict()
    for key in key_list:
        if '=' not in key:
            continue

        for element in data[key]:
            if key not in combined:
                combined[key] = []

            p     = element[1]
            score = element[3]

            combined[key].append([score, p])

    # Combine into final list
    final = dict()
    # Go through all ab
    for key in combined: 
        final[key] = []
        
        # Get individual scores
        A_name, B_name = key.split('=')
        A = individual[A_name]
        B = individual[B_name]

        # Get ab, p pairings
        p_values = combined[key]
    
        # Stitch into final data
        for val in p_values:
            AB = float(val[0])
            p  = float(val[1])
            final[key].append([A,B,AB,p])

    return final

# Accept list of A,B,AB,p
def sim_data(data):
    sim = dict()
    for key in data:
        S = 0.0
        for element in data[key]:
            try:
                num = abs(abs(element[0] - element[2]) - abs(element[1] - element[2]))
                den = abs(element[0] - element[1])
                S += num/den
            except:
                S += 1.0

        S = S/len(data[key])
        sim[key] = S
    
    return sim

def table_data(data):
    # Create name num pairing
    c = 0
    name_val = dict()
    for key in data:
        name = key.split('=')[0]
        if name in name_val:
            continue
        else:
            name_val[name] = c
            c = c + 1
    # Skips taxi, too lazy to fix in general
    name_val['Taxi-v3'] = 9

    # Creat table struct, fill it
    tab = np.zeros((10,10))
    for key in data:
        name  = key.split('=')[0]
        name2 = key.split('=')[1]

        tab[name_val[name]][name_val[name2]] = data[key] 
        tab[name_val[name2]][name_val[name]] = data[key] 

    for i in tab:
        print(i)

    return tab, name_val

def write_data(data, name_val):
    with open('nice_results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        key_list = name_val
        spamwriter.writerow(key_list)

        for ind, key in enumerate(key_list):
            spamwriter.writerow([key] + list(data[ind]))
    

data_raw = load_data()
clean_data = conform_data(data_raw)
sim = sim_data(clean_data)
table,name_val = table_data(sim)

write_data(table,name_val)
print(sim)


