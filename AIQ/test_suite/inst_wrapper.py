import random

class wrap():

    def __init__(self, instA, instB):
        self.instA = instA
        self.instB = instB
        self.instA_in = self.instA.get_header().input_dim
        self.instA_out = self.instA.get_header().output_dim
        self.instB_in = self.instB.get_header().input_dim
        self.instB_out = self.instB.get_header().output_dim

        self.max_in = max(self.instA_in,self.instB_in)
        self.max_out = max(self.instA_out,self.instB_out)

    def select():
        r = random.uniform(0.0, 1.0)
        if r < 0.5:
            self.inst = instA
        else:
            self.inst = instB

    def output_format(self, out):
        if len(out) < len(self.max_out):
            return out + [0.0] * (len(self.max_out) - len(out))
        else:
            return out

    def input_format(self, inp):
        if len(inp) < len(self.max_in):
            return inp + [0.0] * (len(self.max_in) - len(out))
        else:
            return inp

    def reset(self):
        self.select()
        obs = self.inst.reset()
        return self.output_format(obs)

    def step(self, action):
        action = self.input_format(action)
        obs = self.act(action)
        return self.output_format(obs)

    def act(self, action):
        return self.inst.act(action)

    def render(self):
        return self.inst.render()
    
    def get_header():
        return self.inst.get_header()

