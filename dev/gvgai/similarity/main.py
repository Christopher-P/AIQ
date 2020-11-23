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


def evaluate(env_name_1, env_name_2, sample):
    env_1 = gym.make(env_name_1)
    env_2 = gym.make(env_name_2)

    p = sample / 10.0
    env_3 = Merged(env_1, env_2, p=p)
    sample = NeuralNetwork(env_3)
    a = sample.train()
    print(a.history)
    score = a.history['episode_reward']
    steps = a.history['nb_steps']

    log_results([env_name_1, env_name_2, p] + score + steps)

    return None


def main():
    number = int(sys.argv[1])

    # List of envs to test
    titles = ['aliens', 'boulderdash', 'butterflies', 'chase', 'missilecommand', 'survivezombies', 'zelda']

    for ind, val in enumerate(titles):
        titles[ind] = 'gvgai-' + str(val) + '-lvl0-v0'

    # List of p
    p = list(range(11))

    # make every possible combination then decode with input
    c = np.array(np.meshgrid(titles, titles, p))
    c = c.T.reshape(-1, 3)

    name_1, name_2, p = c[number]
    p = int(p)

    # Evaluate the two envs
    evaluate(name_1, name_2, p)

    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    end = time.time()
    print(end-start)
