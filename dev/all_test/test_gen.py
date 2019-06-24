import random
import numpy as np

class join():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.name = str(a.name) + '=' + str(b.name)


    # create an x,y pair according to the brain
    def sample(self, test):
        x = np.random.rand(test.size)
        y = np.dot(x, test.brain)
        return x, y

    # create n samples from the sample function
    def sample_n(self,n):
        x_data = []
        y_data = []
        for i in range(n):
            if random.random() < 0.5:
                x,y = self.sample(self.a)
            else:
                x,y = self.sample(self.b)
            x_data.append(x)
            y_data.append(y)

        return np.asarray(x_data), np.asarray(y_data)
    

class test():

    def __init__(self, size, name):
        # get size from input
        self.size = size

        # create array for holding scalars
        self.create_brain()

        self.name = name

    # create an x,y pair according to the brain
    def sample(self):
        x = np.random.rand(self.size)
        y = np.dot(x, self.brain)
        return x, y

    # create n samples from the sample function
    def sample_n(self,n):
        x_data = []
        y_data = []
        for i in range(n):
            x,y = self.sample()
            x_data.append(x)
            y_data.append(y)

        return np.asarray(x_data), np.asarray(y_data)

    # creats scalar values for inputs
    def create_brain(self):
        # brain holds the key to generating data for test
        self.brain = []

        # fill with random values of -1 to 1
        for i in range(self.size):
            self.brain.append(random.uniform(-1,1))

        # normalize negative numbers
        n_sum = 0.0
        for i in self.brain:
            if i < 0.0:
                n_sum += i

        # Make sure we found a negative number
        if n_sum == 0.0:
            self.create_brain()
            return None
        # do norm
        else:
            for ind,val in enumerate(self.brain):
                if i < 0.0:
                    self.brain[ind] = val / n_sum * -1

        # normalize positive numbers        
        p_sum = 0.0
        for i in self.brain:
            if i > 0.0:
                p_sum += i

        # Make sure we found a negative number
        if p_sum == 0.0:
            self.create_brain()
            return None
        # do norm
        else:
            for ind,val in enumerate(self.brain):
                if i > 0.0:
                    self.brain[ind] = val / n_sum

        self.brain = np.asarray(self.brain)

