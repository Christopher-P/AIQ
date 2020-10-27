#!/usr/bin/env python
# https://github.com/rubenrtorrado/GVGAI_GYM/blob/master/testAgent.py

import gym
import gym_gvgai
import Agent as Agent
import random
random.seed(12)

import time

# Predefined names referring to framework
games = ['gvgai-testgame1', 'gvgai-testgame2', 'gvgai-testgame3']
trainingLevels = ['lvl0-v0', 'lvl1-v0']
testLevels = ['lvl2-v0', 'lvl3-v0', 'lvl4-v0']

for game in games:
    for level in trainingLevels: #testLevels:
        env = gym_gvgai.make(game + '-' + level)
        agent = Agent.Agent()
        print('Starting ' + env.env.game + " with Level " + str(env.env.lvl))
        # reset environment
        stateObs = env.reset()
        actions = env.unwrapped.get_action_meanings()
        start = time.time()
        for t in range(2000):
            # choose action based on trained policy
            action_id = agent.act(stateObs, actions)
            # do action and get new state and its reward
            stateObs, diffScore, done, debug = env.step(action_id)
            print("Action " + str(action_id) + " tick " + str(t+1) + " reward " + str(diffScore) + " win " + debug["winner"])
            #env.render()
            # break loop when terminal state is reached
            if done:
                print(t / (time.time() - start))
                exit()
                break
