### This file will calculate the final AIQ score for the two metrics.
import csv
import sys
import ast

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
    for ind,val in enumerate(ct):
        indvidial_diversity.append(sum(val)/len(val))

    return indvidial_diversity

def get_complexity():
    # Found in complexity/plot.py
    normed_complexity = [0.609375, 0.24390243902439024, 0.33406113537117904, 0.0, 1.627906976744186, 0.14, 0.998856196260945, 0.1582452017234626, 0.02, 0.920575748161955]
    
    sum_normed_complexity = []
    for ind,val in enumerate(normed_complexity):
        sum_normed_complexity.append(val/sum(normed_complexity))
    return sum_normed_complexity

def get_similarity():
    # Load cross table
    data = load_data('sim.csv')

    # Convert to ID
    sim_ID = compute_ID(data)
    return sim_ID

def get_tl():
    file_names = ["Asymptotic.csv", "JumpStart.csv", "Reward.csv", "Ratio.csv"]
    datas = []
    # Load 4 TL methods
    for name in file_names:
        datas.append(load_data(name))

    # Convert to ID
    tl_ID = []
    for i in datas:
        tl_ID.append(compute_ID(i))

    return tl_ID

def get_handicapping():

# Get summed-normed complexity weights
complexity_w = get_complexity()

print("Complexity Weights", complexity_w)

# Get sim data for diversity
similarity = get_similarity()

print("Similarity Weights", similarity)

# Get list of tl approaches for diversity
transfer_learning = get_tl()

print("Similarity Weights", transfer_learning)

# Get Handicapping data
handicapping_p = [[]]


# Run through final AIQ score
