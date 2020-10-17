#!/usr/bin/env python
# https://github.com/rubenrtorrado/GVGAI_GYM/blob/master/testAgent.py

import gym
import gym_gvgai
import Agent as Agent

a = [env.id for env in gym.envs.registry.all() if env.id.startswith('gvgai')]
obs = set()
acts = set()
for name in a:
    try:
        env = gym_gvgai.make(name)
        print(name)
        print("obs:", env.observation_space)
        obs.add(str(env.observation_space))
        print("act:", env.action_space)
        acts.add(str(env.action_space))
    except:
        continue
print(a)
print(obs)
print('==================')
print(acts)
exit()

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
        for t in range(2000):
            # choose action based on trained policy
            action_id = agent.act(stateObs, actions)
            # do action and get new state and its reward
            stateObs, diffScore, done, debug = env.step(action_id)
            print("Action " + str(action_id) + " tick " + str(t+1) + " reward " + str(diffScore) + " win " + debug["winner"])
            env.render()
            # break loop when terminal state is reached
            if done:
                break
