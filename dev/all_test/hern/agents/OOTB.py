# Chris' out of the box agent

from Agent import Agent

from numpy import zeros
from numpy import ones

import  numpy as np

from random import randint, randrange, random

from DQN_backend import DQN_Agent
from collections import deque

class OOTB(Agent):

    def __init__( self, refm, disc_rate, hand ):
        print("HEEEE")

        Agent.__init__( self, refm, disc_rate )

        self.mem = None
        
        self.obs_symbols = refm.getNumObsSyms()
        self.obs_cells   = refm.getNumObsCells()

        # Handicapping amount
        self.agent2 = DQN_Agent(hand)
        inputs = [self.obs_symbols * self.obs_cells]
        outputs = [self.num_actions]
        
        try:
            self.agent2.prepare_agent(inputs,outputs)
            self.agent2.dqn.training = True
        except Exception as e:
            print(e)
            exit()
        
        #self.hand = hand
        self.epsilon = hand
        self.reset()


    def reset( self ):

        self.action = 0

        self.total = zeros( (self.num_actions) )
        self.acts  = ones(  (self.num_actions) )
        self.agent2.dqn.reset_states()
        self.r = True
        self.mem = deque()

    def __str__( self ):
        return "OOTB(" + str(self.epsilon) + ")"


    def perceive( self, observations, reward ):

        if len(observations) != self.obs_cells:
            raise NameError("OOTB:Perceive: recieved wrong number of observations!")

        # convert obs into one hot
        '''
        obs = zeros((self.obs_symbols * self.obs_cells))
        for i in range(self.obs_cells):
           obs[i*self.obs_cells + self.obs_symbols - 1] = 1
        '''
        # convert observations into a single number for the new state
        nstate = 0
        for i in range(self.obs_cells):
           nstate = observations[i] * self.obs_symbols**i

        if len(self.mem) < 10:
            self.mem.appendleft(nstate)
            return randint(0,4)

        if self.r:
            self.r = False
            self.agent2.dqn.backward(reward, True)
        else:
            self.agent2.dqn.backward(reward, False)

        self.mem.appendleft(nstate)
        self.mem.pop()
        print(self.mem)
        tmp = np.asarray(self.mem)
        print(tmp)
        tmp = tmp.reshape(1,10, 1)
        print(tmp, tmp.shape)
        act = self.agent2.dqn.forward(tmp)
        #print(act)
        naction = act

        # update the old action
        self.action = naction

        return naction

