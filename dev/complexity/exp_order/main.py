#/usr/bin/env python3
# Reproducable 
import random
random.seed(123)
import numpy as np
np.random.seed(123)
from tensorflow import set_random_seed
set_random_seed(123)
# end reproducable

import csv 

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Input
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

import datetime
import sys

import gym
from rl.agents import SARSAAgent, DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import EpisodeParameterMemory, SequentialMemory

def gen_model(env_obs, env_act,nodes,layers):
    input_shape = env_obs
    num_classes = env_act

    model = Sequential()
    model.add(Dense(nodes, activation='relu',
              input_shape=(1,input_shape)))

    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count

def run_it(env, nodes, layers):

    # Env info:
    nb_step = 50000
    nb_eps  = 100
    try:
        env_obs = env.observation_space.shape
    except:
        env_obs = env.action_space.n
    try:
        env_act = env.action_space.n
    except:
        env_act = env.action_space.shape

    # Create model with random params, get TP and NTP 
    model, tp, ntp = gen_model(env_obs, env_act, nodes, layers)

    # Setup policy/memory
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=50)

    # Setup RL agent
    dqn = DQNAgent(model=self.model, nb_actions=10, memory=memory, nb_steps_warmup=1000,
                       target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=.00025), metrics=['mae'])

    # Run training
    dqn.fit(env, nb_steps=nb_step, visualize=False, verbose=1)

    # Run testing
    scores = dqn.test(env, nb_episodes=nb_eps, visualize=False)

    # Grab score data
    results = np.mean(scores.history['episode_reward'])
    print(type(results))

    return results, tp, ntp


def log_it(results):
    with open('data/results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)

def main():
    # Setup env selections
    names = ['CartPole-v0', 'Acrobot-v1', 'FrozenLake-v0', 'FrozenLake8x8-v0']
    # Init envs
    envs = []
    for name in names:
        envs.append(gym.make(name))
        envs[-1].reset()

    # Overide acrobot
    #from acrobot import AcrobotEnv
    #tmp_env = AcrobotEnv()
    #envs[0] = tmp_env

    for j in range(1000):
        for i in range(len(names)):
            # get random network params
            nodes  = 300#int(random.random() * 32) + 1
            layers = 5#int(random.random() * 5) + 1

            # Run exp
            results, tp, ntp  = run_it(envs[i], nodes, layers)

            # Save exp
            print(names[i], results)
            log_it([names[i]] + [nodes, layers, tp, ntp] + [results])

    return None

if __name__ == '__main__':
    ## Parse args here
    main()
