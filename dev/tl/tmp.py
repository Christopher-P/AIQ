import gym

env = gym.make('CartPole-v0')
env.reset()
while True:
    t = input()
    env.render()
    a, b, c, d = env.step(int(t))
    print(a,b,c,d)
