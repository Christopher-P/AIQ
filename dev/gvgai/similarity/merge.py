#!usr/bin/env python3


# This class takes in two open ai gym envs and creates a new one from them merged
class Merged:

    def __init__(self, instA, instB, p):
        # Save to local
        self.instA = instA
        self.instB = instB
        self.p = p

        # Proccess test params
        self.instA_in = self.instA.get_header().input_dim
        self.instA_out = self.instA.get_header().output_dim
        self.instB_in = self.instB.get_header().input_dim
        self.instB_out = self.instB.get_header().output_dim

        self.max_in = max(self.instA_in, self.instB_in)
        self.max_out = max(self.instA_out, self.instB_out)
        self.header = header(self.instA.get_header().env_name + "=" +
                             self.instB.get_header().env_name,
                             self.max_in,
                             self.max_out,
                             -1, "empty", True, -200, 200)

    # random sampling
    def select(self):
        r = random.uniform(0.0, 1.0)
        if r < self.p:
            self.inst = self.instA
        else:
            self.inst = self.instB

    def output_format(self, out):
        if len(out) < self.max_out[0]:
            result = np.zeros(self.max_out[0])
            result[0:len(out)] = out
            # print(out, result)
            return result
        else:
            return out

    def input_format(self, inp):
        # print(inp,self.inst.get_header().input_dim)
        if inp > self.inst.get_header().input_dim - 1:
            return self.inst.get_header().input_dim - 1
        else:
            return inp

    def reset(self):
        self.select()
        obs = self.inst.reset()
        obs = self.output_format(obs)
        return obs

    # Calls act
    def step(self, action):
        return self.act(action)

    def act(self, action):
        action = self.input_format(action)
        # print(self.inst.act(action))
        obs, r, done, info = self.inst.act(action)
        obs = self.output_format(obs)
        return obs, r, done, info

    def render(self):
        return self.inst.render()


