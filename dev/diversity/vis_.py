import gym
import time
env = gym.make("Adventure-v0")
observation = env.reset()
for _ in range(1000):
  env.render()
  action = env.action_space.sample() # your agent here (this takes random actions)
  observation, reward, done, info = env.step(action)
  time.sleep(1)

  if done:
    observation = env.reset()
env.close()

