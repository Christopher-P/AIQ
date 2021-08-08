import gym
import gym_gvgai

import random
random.seed(12)
import csv
import time

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam
from keras import backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory

from os import listdir
from os.path import isfile, join

def create_model(name, nodes, layers):
    # Create env
    env = gym_gvgai.make(name)

    # Get obs_size
    obs = env.reset()
    obs_size = len(obs)


    # Next, we build a very simple model.
    model = Sequential()
    model.add(Flatten(input_shape=(4, obs_size)))

    # Variable network
    for _ in range(layers):
        model.add(Dense(nodes))
        model.add(Activation('relu'))

    model.add(Dense(len(env.actions)))
    model.add(Activation('linear'))
    print(model.summary())

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=50000, window_length=4)
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.0, value_test=.05,
                                  nb_steps=1000000)
    dqn = DQNAgent(model=model, nb_actions=len(env.actions), policy=policy, memory=memory,
                   nb_steps_warmup=50000, gamma=.99, target_model_update=10000,
                   train_interval=4, delta_clip=1.)
    dqn.compile(Adam(lr=.00025), metrics=['mae'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return trainable_count, non_trainable_count


# Load data from data dir

# Get all file paths
data_path = './data/'
file_names = [f for f in listdir(data_path) if isfile(join(data_path, f))]

# Open every file
for file_name in file_names:
    print(file_names)
    with open(data_path + file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # Name, nodes, layers, TP, NTP, score
            task_name = row[0]
            nodes = int(row[1])
            layers = int(row[2])
            rest = row[3:]

            # Back create tp, ntp
            tp, ntp = create_model(task_name, nodes, layers)

            with open('data_fix.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([task_name, nodes, layers, tp, ntp] + rest)

