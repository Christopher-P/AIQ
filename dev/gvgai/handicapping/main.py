import sys
import csv
import time
import random

import numpy as np

import gym
import gym_gvgai

from merge import Merged
from agent import NeuralNetwork


def log_results(time, data):
    with open('data' + str(time) + '.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data)
    return None


def evaluate(env_name_1, nodes, layers, seed):
    env_1 = gym.make(env_name_1)

    sample = NeuralNetwork(env_1, nodes, layers, seed=seed)
    a, tp, ntp = sample.train()
    scores = a.history['episode_reward'][-5:]
    results = sum(scores) / len(scores)
    steps = a.history['nb_steps']

    return results, tp, ntp


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
            print(int(start), [i] + [nodes, layers, tp, ntp] + [score])
            log_results(int(start), [i] + [nodes, layers, tp, ntp] + [score])

    return None


if __name__ == "__main__":
    main()
