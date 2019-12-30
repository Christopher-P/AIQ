# Compare diversity equation utilizing the TL dataset and Sim Dataset
import csv
import copy

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def load_data(file_name):
    data = []
    with open('data/' + file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in spamreader:
            data.append(row)

    # Since data has row/col headers, remove
    data_slice = [data[i][1:11] for i in range(1,11)]
    return data_slice

# Accept list of ID
def plot(data, graph_name, axs, isMin):
    names = ["CartPole-v0", "CartPole-v1", "Acrobot-v1",
            "MountainCar-v0", "Roulette-v0","FrozenLake-v0",
             "CliffWalking-v0","NChain-v0","FrozenLake8x8-v0", "Taxi-v2"]

    # Sort data
    data, names = (list(t) for t in zip(*sorted(zip(data, names))))
    y_pos = np.arange(len(names))
    
    if isMin:
        graph_name = 'min - ' + graph_name
    else:
        graph_name = 'avg - ' + graph_name

    if axs is None:
        plt.bar(y_pos, data, align='center', alpha=0.5)
        plt.xticks(y_pos, names,rotation=45)
        plt.ylabel('ID')
        plt.title(graph_name)
        plt.savefig('graphs/' + graph_name  + '.png')
        plt.show()

    else:
        axs.bar(y_pos, data, align='center', alpha=0.5)
        # X Axis
        plt.setp(axs.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
        axs.set_xticks(np.arange(10))
        axs.set_xticklabels(names)
        # Y Axis
        axs.set_yticks(np.arange(0,0.8, 0.2))
        axs.set_ylabel('ID')
        axs.set_title(graph_name)

    return axs


# Individual Diversity
# Expect data formated as nice_results.csv
# Note: Similarity is dissimalarity (1-sim) form!
# Run over TL, SIM
names = ['Asymptotic.csv', 'JumpStart.csv', 'Ratio.csv', 'Reward.csv', 'sim.csv']




plot_single = True

if not plot_single:
    # Setup graph
    fig, axs = plt.subplots(5, 2, figsize=(20,10))

# Do for all variations of tl and sim
for ind2, name in enumerate(names):

    data = load_data(name)

    # Conver data to floats!
    for i,v in enumerate(data):
        for j,w in enumerate(v):
            data[i][j] = float(w)
    
    # Smallest similarity between tests
    min_ids = []
    for ind, row in enumerate(data):
        # Exclude self (diaganol)
        t_d = row[:ind] + row[ind+1:]
        min_ids.append(min(t_d))
    
    # Average similarity between tests
    avg_ids = []
    for row in data:
        avg_ids.append(sum(row)/len(row))

    # Normalize between 0.0 and 1.0
    tmp = copy.deepcopy(min_ids)
    for ind, val in enumerate(tmp):
        min_ids[ind] = (val - min(tmp)) / (max(tmp) - min(tmp))
    tmp = copy.deepcopy(avg_ids)
    for ind, val in enumerate(tmp):
        avg_ids[ind] = (val - min(tmp)) / (max(tmp) - min(tmp))

    # The sum of all test ID should be 1.0
    # Do normalization here
    tmp = copy.deepcopy(min_ids)
    for ind, val in enumerate(tmp):
        min_ids[ind] = val / sum(tmp)
    tmp = copy.deepcopy(avg_ids)
    for ind, val in enumerate(tmp):
        avg_ids[ind] = val / sum(tmp)
    print(ind2)

    if plot_single:
        ## The following save to high res single plot
        # Plot mins
        plot(min_ids, name, None, True)
        # Plot avgs
        plot(avg_ids, name, None, False)
    else:
        # Plot mins
        plot(min_ids, name, axs[ind2,0], True)

        # Plot avgs
        plot(avg_ids, name, axs[ind2,1], False)



    #exit()

fig.tight_layout()
plt.savefig('Results.png', dpi=600)

#plt.show() 

