#!/usr/bin/env python
# https://github.com/rubenrtorrado/GVGAI_GYM/blob/master/testAgent.py

import gym
import gym_gvgai
from sarsa.Agent import Agent
import random
random.seed(12)
import csv
import time


def log_results(time, data):
    with open('data' + str(time) + '.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data)
    return None


def main():
    for _ in range(1000):
        start = time.time()

        # List of envs to test
        titles = ['butterflies', 'chase', 'zelda', 'testgame1', 'aliens', 'boulderdash', 'missilecommand', 'survivezombies']

        for ind, val in enumerate(titles):
            titles[ind] = 'gvgai-' + str(val) + '-lvl0-v0'

        for i in titles:
            # Create env
            env = gym_gvgai.make(i)

            # Number of train eps
            train_eps = 5 #int(random.random() * 6)
            test_eps = 1

            # Create sarsa Agent
            sarsa = Agent()
            sarsa.init(env.GVGAI.sso, None, train_eps - 2)

            # Train agent
            for episode in range(train_eps):
                env.reset()
                is_done = False
                for t in range(2000):
                    # choose action based on trained policy
                    action_id = sarsa.act(env.GVGAI.sso, None)
                    if action_id == 'ACTION_ESCAPE':
                        action_id = 0

                    # do action and get new state and its reward
                    stateObs, diffScore, is_done, debug = env.step(action_id)
                    print("Action " + str(action_id) + " reward " + str(env.GVGAI.sso.gameScore) + " win " +
                          debug["winner"])

                sarsa.result(env.GVGAI.sso, None)

            # Test agent
            for episode in range(test_eps):
                env.reset()
                reward = 0.0
                is_done = False
                for t in range(2000):
                    # choose action based on trained policy
                    action_id = sarsa.act(env.GVGAI.sso, None)
                    if action_id == 'ACTION_ESCAPE':
                        action_id = 0

                    # do action and get new state and its reward
                    stateObs, diffScore, is_done, debug = env.step(action_id)
                    print("Action " + str(action_id) + " reward " + str(env.GVGAI.sso.gameScore) + " win " +
                          debug["winner"])

                    reward = reward + diffScore

                sarsa.result(env.GVGAI.sso, None)

            log_results(int(start), [i, reward/test_eps, train_eps])
            exit()
    return None


if __name__ == "__main__":
    main()
