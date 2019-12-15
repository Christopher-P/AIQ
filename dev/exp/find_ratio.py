# Used to find the Ratio that was supposed to be recorded.
# Can be removed after data is regathered
# Results of experiment stored in raw

import csv
import ast

# Standard load function
def load_file(filename):
    data = []
    with open('data_bak/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        for row in spamreader:
            data.append((row[0], row[1], row[2], row[3]))

    return data

# Takes a list of values, returns the area under the curve
def AuC(data):

    Area = 0.0

    for ind,val in enumerate(data):

        # Dont do last value
        if ind >= len(data) - 1:
            continue
        
        # Calculate box area
        h = min(data[ind], data[ind+1])
        w = 1       # Assume constant width for now

        box_area = h*w

        # Calculate triangle area
        h = max(data[ind], data[ind+1]) - min(data[ind], data[ind+1])
        w = 1       # Assume constant width for now
        
        triangle_area = h*w/2.0

        # Add box and triangle to area
        Area += box_area + triangle_area

    return Area

# Uniform function to save experimental data
def record(filename, nameA, nameB, values, values2=None):
    with open('data/' + filename, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        if values2 == None:
            spamwriter.writerow((nameA, nameB, values))
        else:
            spamwriter.writerow((nameA, nameB, values, values2))
    return None

data = load_file('RAW.csv')

for entry in data:
    # Get names from data
    name_A = entry[0]
    name_B = entry[1]

    # Get dictionary from data
    history_A = lit = ast.literal_eval(entry[2])
    history_B = lit = ast.literal_eval(entry[3])

    A_r = history_A['episode_reward']
    B_r = history_B['episode_reward']

    # Record Transfer Ratio
    # (AuC_B - AuC_A) / AuC_A
    try:
        Ratio = (AuC(B_r) - AuC(A_r)) / AuC(A_r)
    except Exception as e:
        print(A_r)
        Ratio = 0

    record('Ratio.csv', name_A, name_B, Ratio)

