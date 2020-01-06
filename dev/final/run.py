### This file will calculate the final AIQ score for the two metrics.
import csv
import sys
import ast
import copy

import hashlib

## increase max read (big data files need this)
csv.field_size_limit(sys.maxsize)

def load_data_raw(file_name):
    data = []
    with open('data/' + file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        for row in spamreader:
            data.append(ast.literal_eval(row[1]))

    return data


def load_data(file_name):
    data = []
    with open('data/' + file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in spamreader:
            data.append(row)

    # Since data has row/col headers, remove
    data_slice = [data[i][1:11] for i in range(1,11)]
    
    # Cast to float
    for ind,val in enumerate(data_slice):
        for ind2, val2 in enumerate(val):
            data_slice[ind][ind2] = float(val2)


    return data_slice

# Accept cross table for similarities
def compute_ID(ct):
    # List for holding new data
    indvidial_diversity = []

    # Find avg ID
    for ind,val in enumerate(ct):
        indvidial_diversity.append(sum(val)/len(val))

    # Shift all values up to positive
    for ind,val in enumerate(indvidial_diversity):
        indvidial_diversity[ind] = val + abs(min(indvidial_diversity))

    # Sum-Normalize IDs
    tmp_ = copy.deepcopy(indvidial_diversity)
    for ind,val in enumerate(tmp_):
        indvidial_diversity[ind] = val / sum(tmp_)

    return indvidial_diversity

def get_complexity():
    # Found in complexity/plot.py
    normed_complexity = [0.609375, 0.24390243902439024, 0.33406113537117904, 0.0, 1.627906976744186, 0.14, 0.998856196260945, 0.1582452017234626, 0.02, 0.920575748161955]

    # Remove mountain-car
    normed_complexity = normed_complexity[:3] + normed_complexity[4:]

    #print(normed_complexity)
    #exit()
    sum_normed_complexity = []
    for ind,val in enumerate(normed_complexity):
        sum_normed_complexity.append(val/sum(normed_complexity))
    return sum_normed_complexity

def get_similarity():
    # Load cross table
    data = load_data('sim.csv')

    # Remove mountain car
    data = data[:3] + data[4:]

    # Convert to ID
    sim_ID = compute_ID(data)
    return sim_ID

def get_tl():
    file_names = ["Asymptotic.csv", "JumpStart.csv", "Reward.csv", "Ratio.csv"]
    datas = []
    # Load 4 TL methods
    for name in file_names:
        datas.append(load_data(name))

    # Normalize CT
    #for i in range(len(datas)):
    #    datas[i] = normalize_ct(datas[i])

    # Convert to ID
    tl_ID = []
    for i in datas:
        tl_ID.append(compute_ID(i))

    return tl_ID

def get_handicapping():
    data = []
    with open('data/handicapping.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        for row in spamreader:
            if row[0] == "MountainCar-v0":
                continue
            data.append([row[0],row[1],float(row[2])])
    return data

def normalize_ct(ct):
    max_c = -9999999999999
    min_c = 99999999999999

    for i in range(len(ct)):
        for j in range(len(ct[i])):
            if max_c < ct[i][j]:
                max_c = ct[i][j]
            if min_c > ct[i][j]:
                min_c = ct[i][j]

    print(max_c,min_c)

    tmp_ct = copy.deepcopy(ct)
    for i in range(len(ct)):
        for j in range(len(ct[i])):
            tmp_ct[i][j] = (ct[i][j] - min_c) / (max_c - min_c)

    return tmp_ct


def compute_AIQ(P, C, ID):
    # Compute diversity from individual diversities
    D = sum(ID)

    # Calculate AIQ
    s = 0.0
    #print("D",D)
    for i in range(len(P)):
        #print(type(P[i][2]), C[i])
        s = s + P[i][2] * C[i]
    AIQ = s * D
    return AIQ

def save_data(results):
    with open('results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for i in results:
            spamwriter.writerow(i)

# Get summed-normed complexity weights
complexity_w = get_complexity()

print("Complexity Weights", complexity_w)

# Get sim data for diversity
similarity = get_similarity()

print("Similarity Weights", similarity)

# Get list of tl approaches for diversity
transfer_learning = get_tl()

for i in transfer_learning:
    print("Transfer Weights", i)

# Get Handicapping data
handicapping_p = get_handicapping()

#print("Similarity Weights", handicapping_p)

# Names to save data as
file_names = ["Asymptotic", "JumpStart", "Reward", "Ratio", "Sim"]
transfer_learning.append(similarity)

results = []

# Run through final AIQ score
for j in range(5):
    for i in range(10):
        AIQ = compute_AIQ(handicapping_p[i*9:(i*9)+9], complexity_w, transfer_learning[j])
        results.append((file_names[j], AIQ, i*10 ))

save_data(results)
