import sys
import csv
import time
import random

import gym
import gym_gvgai

from merge import Merged
from agent import NeuralNetwork


def log_results(data):
    with open('results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data)
    return None


def evaluate(env_name_1, env_name_2):
    env_1 = gym.make(env_name_1)
    env_2 = gym.make(env_name_2)

    for p in range(10):
        env_3 = Merged(env_1, env_2, p=p/10.0)
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

    name_1 = titles[int(number / 7)]
    name_2 = titles[int(number % 7)]

    # Evaluate the two envs
    evaluate(name_1, name_2)

    return None


if __name__ == "__main__":
    main()
