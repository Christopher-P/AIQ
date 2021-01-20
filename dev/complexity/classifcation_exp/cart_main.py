#/usr/bin/env python3

from test_loader import Loader
import csv 
import time

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Input, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.optimizers import Adam

import random
import numpy as np
import gym

import datetime
import sys

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

def gen_model(data, nodes, layers):
    input_shape = (4, 1)
    num_classes = 2

    model = Sequential()
    model.add(Flatten(input_shape=(1,) + (4, )))
    model.add(Dense(nodes))
    model.add(Activation('relu'))

    for i in range(layers - 1):
        model.add(Dense(nodes))
        model.add(Activation('relu'))

    model.add(Dense(2))
    model.add(Activation('linear'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count


def run_it(nodes, layers):
    env = gym.make('CartPole-v0')
    results = []

    model, tp, ntp = gen_model(i, nodes, layers)

    memory = SequentialMemory(limit=50000, window_length=1)
    policy = BoltzmannQPolicy()
    dqn = DQNAgent(model=model, nb_actions=2, memory=memory, nb_steps_warmup=10,
                   target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

    # Finally, evaluate our algorithm for 5 episodes.
    a = dqn.test(env, nb_episodes=10, visualize=False)
    score = a.history['episode_reward']
    perf = sum(score) / len(score)

    results.append(perf)

    return results, tp, ntp


def log_it(name, results):
    with open('cart_data/' + str(name) + '.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)


def main(start):
    # Number of samples (all domains)
    samples = 100

    # Get time for seed and file_name
    time = str(start)

    # Seed it
    random.seed(start)
    np.random.seed(int(start))

    for j in range(samples):
        nodes = int(random.random() * 32) + 1
        layers = int(random.random() * 5) + 1
        results, tp, ntp = run_it(nodes, layers)
        print(time, ["CARTPOLE-RL"] + [nodes, layers, tp, ntp] + results)
        log_it(time, ["CARTPOLE-RL"] + [nodes, layers, tp, ntp] + results)

    return None


if __name__ == '__main__':
    ## Parse args here
    for i in range(1000):
        start = time.time()
        np.random.seed(int(start))
        main(start)
        done = time.time()
        elapsed = done - start
        print(elapsed)
