#/usr/bin/env python3

import csv 
import time

import gym

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import random
import numpy as np

import datetime
import sys


def gen_model(nodes, layers):
    input_shape = (1, 4)
    num_classes = 2

    model = Sequential()
    model.add(Dense(nodes, activation='relu',
              input_shape=input_shape))

    for i in range(layers - 1):
        model.add(Dense(nodes, activation='relu'))

    model.add(Flatten())
    model.add(Dense(num_classes, activation='linear'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count


def run_it(nodes, layers):

    # Experiment Vars
    samples = 200000

    ENV_NAME = 'CartPole-v0'
    env = gym.make(ENV_NAME)

    results = []
    model, tp, ntp = gen_model(nodes, layers)
    memory = SequentialMemory(limit=50000, window_length=1)
    policy = BoltzmannQPolicy()
    dqn = DQNAgent(model=model, nb_actions=2, memory=memory, nb_steps_warmup=10,
                   target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    dqn.fit(env, nb_steps=samples, visualize=False, verbose=1)
    scores = dqn.test(env, nb_episodes=5, visualize=False)
    results = sum(scores.history['episode_reward']) / len(scores.history['episode_reward'])
    print(results)

    return results, tp, ntp


def log_it(name, results):
    with open('data/' + str(name) + '_cart.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)


def main(start):
    # Number of samples (all domains)
    samples = 10

    # Get time for seed and file_name
    time = str(start)

    # Seed it
    random.seed(start)
    np.random.seed(int(start))

    names = ['CARTPOLE']

    for j in range(samples):
        for i in range(len(names)):
            nodes = int(random.random() * 32) + 1
            layers = int(random.random() * 5) + 1
            results, tp, ntp = run_it(nodes, layers)
            print(time, [names[i]] + [nodes, layers, tp, ntp] + [results])
            log_it(time, [names[i]] + [nodes, layers, tp, ntp] + [results])

    return None


if __name__ == '__main__':
    ## Parse args here
    for i in range(200):
        start = time.time()
        main(start)
        done = time.time()
        elapsed = done - start
        print(elapsed)
