#!/usr/bin/env python
# https://github.com/rubenrtorrado/GVGAI_GYM/blob/master/testAgent.py

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

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory


def log_results(time, data):
    with open('data' + str(time) + '.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(data)
    return None


def main():
    for _ in range(1000):
        start = time.time()

        # List of envs to test
        titles = ['butterflies', 'zelda', 'chase', 'testgame1', 'aliens', 'boulderdash', 'missilecommand', 'survivezombies']

        for ind, val in enumerate(titles):
            titles[ind] = 'gvgai-' + str(val) + '-lvl0-v0'

        for i in titles:
            # Random nn
            nodes = int(random.random() * 10 + 1) * 32
            layers = int(random.random() * 5) + 1

            # Create env
            env = gym_gvgai.make(i)

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

            # Okay, now it's time to learn something! We visualize the training here for show, but this
            # slows down training quite a lot. You can always safely abort the training prematurely using
            # Ctrl + C.
            dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

            # Finally, evaluate our algorithm for 5 episodes.
            history = dqn.test(env, nb_episodes=5, visualize=False)
            results = history.history['episode_reward']
            score = sum(results)/len(results)

            log_results(int(start), [i, score])

    return None


if __name__ == "__main__":
    main()
