# OpenSource BlocksWorld simulator
# The goal is to place all the blocks on
# the set spot with blocks from (A-top to Z-bot)

# v0 will use random placement for blocks in the world
# v0 will assume goal stack is right-most column
# v0 scores off euclidean

import random
import math

# http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaStackinPython.html
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class Simulator():

    def __init__(self, world_size, blocks, score, limit):
        self.world_size = world_size
        self.blocks = blocks
        self.score_function = score
        self.is_done = None
        self.hand = None
        self.holding = None
        self.time = None
        self.limit = limit

    def get_done_state(self):
        goals = []
        for ind in range(self.blocks):
            goals.append((self.alphabet(ind), self.world_size - 1, self.blocks - ind - 1))

        return goals

    def get_world_state(self):
        states = []
        for ind,val in enumerate(self.world):
            for ind2, val2 in enumerate(val.items):
                states.append((val2, ind,ind2))

        return states

    def check_done(self):
        # Check if time limit passed
        if self.time >= self.limit:
            return True

        # Check if goal state achieved
        goal = self.get_done_state()
        world = self.get_world_state()
        if goal == world:
            return True

        # Otherwise its not done
        return False

    def act(self, action):
        # Expects number
        # 1 = move left
        if action == 0:
            if self.hand > 0:
                self.hand -= 1

        # 2 = move right
        if action == 1:
            if self.hand < self.world_size - 1:
                self.hand += 1

        # 3 = grab
        if action == 2:
            if self.holding == None:
                if self.world[self.hand].size() > 0:
                    self.holding = self.world[self.hand].pop()

        # 4 = release
        if action == 3:
            if self.holding is not None:
                self.world[self.hand].push(self.holding)
                self.holding = None
        
        if self.check_done()
            self.is_done = true

        return self.obs()

    def score(self):
        states = []
        for ind,val in enumerate(self.world):
            for ind2, val2 in enumerate(val.items):
                states.append((val2, ind,ind2))
        
        goals = []
        for ind in range(self.blocks):
            goals.append((self.alphabet(ind), self.world_size - 1, self.blocks - ind - 1))
        
        states.sort(key=lambda tup: tup[0])
        res = 0

        for ind, val in enumerate(states):
            res += math.sqrt(math.pow(states[ind][1] - goals[ind][1], 2)
                           + math.pow(states[ind][2] - goals[ind][2], 2))
        res /= self.blocks

        return res


    def reset(self):
        # reset done bool
        self.is_done = False
        # reset hand state
        self.hand = 0
        # clear holding
        self.holding = None
        # Reset time
        self.time = 0
        # generate new world
        self.gen()

    def obs(self):
        info = []
        info.append(self.hand)
        info.append(self.holding)
        info.append(self.score())
        info.append(self.world_state())
        return info

    def world_state(self):
        state = []
        for place in self.world:
            state.append(place.items)
        return state
        
    def gen(self):
        world = None
        world = []

        # Create empty world
        for size in range(self.world_size):
            world.append(Stack())

        # Fill world with blocks
        for block in range(self.blocks):
            location = random.randint(0, self.world_size - 1)
            world[location].push(self.alphabet(block))

        self.world = world
    
    def alphabet(self, num):
        alph = "abcdefghijklmnopqrstuvwxyz"
        return alph[num]
        
env = Simulator(5, 5, None, None)
env.reset()
print(env.obs())
print(env.score())


