import gym
env = gym.make('MountainCar-v0')
env.reset()
for _ in range(1000):
    env.render()
    print(env.action_space)
    env.step(2) # take a random action
env.close()

