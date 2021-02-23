import sys
import csv
import time
import random

import numpy as np

import gym
import gym_gvgai

from merge import Merged
from agent import NeuralNetwork


def log_results(data):
    with open('results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data)
    return None


def evaluate(env_name_1, nodes, layers, seed):
    env_1 = gym.make(env_name_1)

    #print(dir(env_1.env))
    #print(env_1.env.actions)

    sample = NeuralNetwork(env_1, nodes, layers, seed=seed)
    a, tp, ntp = sample.train()
    score = a.history['episode_reward']
    steps = a.history['nb_steps']

    return score, tp, ntp


def main():
    for _ in range(1000):
        start = time.time()
        np.random.seed(int(start))

        # List of envs to test
        titles = ['aliens', 'boulderdash', 'butterflies', 'chase', 'missilecommand', 'survivezombies', 'zelda']

        for ind, val in enumerate(titles):
            titles[ind] = 'gvgai-' + str(val) + '-lvl0-v0'

        for i in titles:
            nodes = int(random.random() * 32) + 1
            layers = int(random.random() * 5) + 3

            # Evaluate the two envs
            score, tp, ntp = evaluate(i, nodes, layers, int(start))
            print(start, [i] + [nodes, layers, tp, ntp] + score)
            log_it(start, [i] + [nodes, layers, tp, ntp] + score)

    return None


if __name__ == "__main__":
    main()
