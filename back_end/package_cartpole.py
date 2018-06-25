import gym
import _pickle as cPickle
from aiq import AIQ

env = gym.make('CartPole-v0')
aiq_cartpole = AIQ(env)

pickle_out = open("CartPole-v0.pickle","wb")
cPickle.dump(aiq_cartpole.getInfo(), pickle_out)
pickle_out.close()
 