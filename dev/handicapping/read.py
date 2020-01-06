import csv
import ast

def save_data(data):
    with open('data/handicapping.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for i in data:
            spamwriter.writerow(i)

def load_data():
    data = []
    with open('data/RAW.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|', quotechar=' ')
        c = 0
        remove = [100,101,102]
        for row in spamreader:
            # Few extra values that were created in error
            if c in remove:
                c = c + 1
                continue
            data.append([row[0], float(row[1]), ast.literal_eval(row[2])['episode_reward'] ])
            for ind,val in enumerate(data[-1][2]):
                data[-1][2][ind] = float(val)
            c = c + 1

    return data

def plot():

    return None

# Gets the max or avg_max of the data
def simplify_data(data):

    # Set number of instances to average over
    samples = 50

    for ind,val in enumerate(data):
        # These envs need to be averaged
        avg_envs = ["Roulette-v0", "FrozenLake-v0","FrozenLake8x8-v0"]

        # Do avg
        if val[0] in avg_envs:
            tmp_arr = val[2][0:samples]
            max_avg = -999999999
            c = 0
            for j in val[2][samples:]:
                if sum(tmp_arr)/len(tmp_arr) > max_avg:
                    max_avg = sum(tmp_arr)/len(tmp_arr)
                tmp_arr[c] = j
                c = c + 1
                if c >= samples:
                    c = 0

            data[ind][2] = max_avg

        # Do simple max
        else:
            data[ind][2] = max(val[2])

    return data

def normalize_data(data):
    scales = [(15.0, 200.0), (15.0, 500.0), (-699.0, -42.0), (-399.0, -110.0), (-71.0, 144.0), (0.0, 1.0), (-26058.0, -10.0), (1318.0, 3677.0), (0.0, 1.0), (-1164.0, 9.7)]
    
    for i in range(len(data)):
        print(data[i])
        data[i][2] = (data[i][2] - scales[i % 10][0]) / (scales[i % 10][1] - scales[i % 10][0])

    return data

# Load data from raw
data = load_data()

# Simplify the data
data = simplify_data(data)

# Normalize data 
data = normalize_data(data)

# Save better data to csv
save_data(data)

print(data)
