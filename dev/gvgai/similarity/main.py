import random

import gym
import gym_gvgai

from merge import Merged

# sample names
name1 = "gvgai-bait-lvl0-v0"
name2 = "gvgai-bait-lvl1-v0"
name3 = "gvgai-bait-lvl2-v0"

# sample envs
env1 = gym_gvgai.make(name1)
env2 = gym_gvgai.make(name2)
env3 = gym_gvgai.make(name3)

env4 = Merged(env1, env2, p=0.5)
env = env4

# reset environment
stateObs = env.reset()
actions = env.inst.actions
for t in range(2000):
    # choose action based on trained policy
    a = random.randrange(len(actions))
    # do action and get new state and its reward
    stateObs, diffScore, done, debug = env.step(a)
    print(stateObs, diffScore, done, debug)
    env.render()
    # break loop when terminal state is reached
    if done:
        break