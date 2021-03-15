#!/usr/bin/env python
# https://github.com/rubenrtorrado/GVGAI_GYM/blob/master/testAgent.py

import gym
import gym_gvgai
from sarsa.Agent import Agent
import random
random.seed(12)

import time

# Predefined names referring to framework
games = ['gvgai-butterflies', 'gvgai-testgame2', 'gvgai-testgame3']
trainingLevels = ['lvl0-v0', 'lvl1-v0']
testLevels = ['lvl2-v0', 'lvl3-v0', 'lvl4-v0']

for game in games:
    for level in trainingLevels: #testLevels:
        env = gym_gvgai.make(game + '-' + level)
        sarsa = Agent()
        print('Starting ' + env.env.game + " with Level " + str(env.env.lvl))
        # reset environment
        stateObs = env.reset()
        actions = env.unwrapped.get_action_meanings()
        start = time.time()

        # Create sarsa Agent
        sarsa.init(env.GVGAI.sso, None)

        for episode in range(10):
            for t in range(2000):
                # choose action based on trained policy
                action_id = sarsa.act(env.GVGAI.sso, None)
                if action_id == 'ACTION_ESCAPE':
                    action_id = 0
                # do action and get new state and its reward
                stateObs, diffScore, done, debug = env.step(action_id)
                print("Action " + str(action_id) + " tick " + str(t+1) + " reward " + str(diffScore) + " win " + debug["winner"])

            sarsa.result(env.GVGAI.sso, None)
            print(str(episode) + " : done!")