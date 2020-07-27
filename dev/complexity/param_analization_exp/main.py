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
from keras.layers import Dense, Dropout, Flatten, Input, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras import backend as K

import datetime
import sys

import gym
from rl.agents import SARSAAgent, DQNAgent
from rl.policy import EpsGreedyQPolicy, BoltzmannQPolicy
from rl.memory import EpisodeParameterMemory, SequentialMemory

def gen_model(env_obs, env_act, nodes,layers):
    input_shape = env_obs
    num_classes = env_act

    model = Sequential()
    model.add(Flatten(input_shape=(1,4)))

    for i in range(layers - 1):
        model.add(Dense(nodes))
        model.add(Activation('relu'))

    model.add(Dense(num_classes))
    model.add(Activation('linear'))
    print(model.summary())
    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    return model, trainable_count, non_trainable_count

def run_it(env, nodes, layers):

    # Env info:
    nb_step = 50000
    nb_eps  = 100
    env_obs = env.observation_space.shape[0]
    env_act = env.action_space.n

    print(env_obs, env_act)

    # Create model with random params, get TP and NTP 
    model, tp, ntp = gen_model(env_obs, env_act, nodes, layers)

    # Setup policy/memory
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    
    # Setup RL agent
    dqn = DQNAgent(model=model, nb_actions=env_act, memory=memory, nb_steps_warmup=10,
               target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    # Run training
    dqn.fit(env, nb_steps=nb_step, visualize=False, verbose=1)

    # Run testing
    scores = dqn.test(env, nb_episodes=nb_eps, visualize=False)

    # Grab score data
    results = np.mean(scores.history['episode_reward'])

    return results, tp, ntp


def log_it(results):
    with open('data/results.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(results)

def main():
    # Setup env selections
    name = 'CartPole-v0'

    # Overide gym
    from cartpole import CartPoleEnv

    for i in range(50):
        # Vary params:
        #gravity = 9.8 / 4 * j 

        # Number of random samples per param
        samples = 50

        # Create inst with custom gravity
        #env = CartPoleEnv(gravity)
        #env = gym.make('CartPole-v0')

        for j in range(1, 21):
            pole = float(j)
            env = CartPoleEnv(pole)

            # get random network params
            nodes  = int(random.random() * 32) + 1
            layers = int(random.random() * 5) + 1

            # Run exp
            results, tp, ntp  = run_it(env, nodes, layers)

            # Save exp
            print(name, results)
            log_it([name, pole] + [nodes, layers, tp, ntp] + [results])

    return None

if __name__ == '__main__':
    ## Parse args here
    main()
