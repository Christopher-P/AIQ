import gym
import _pickle as cPickle
import aiq as AIQ

env = gym.make('CartPole-v0')
aiq_cartpole = AIQ.AIQ(env)

pickle_out = open("CartPole-v0.pickle","wb")
cPickle.dump(aiq_cartpole, pickle_out)
pickle_out.close()
