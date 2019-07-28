# Implemention of random agent
import numpy as np

class R_Agent():

    def __init__(self):
        return None

    # Called for RL type tests
    def act(self, header, data):
        # Ignore data because this is a random agent!
        size = header.input_dim
        return np.random.choice(size[0], 1)
    
    # Called for DS type tests
    def predict(self, header, data):
        #TODO: Generalize for various DS problems
        size = header.output_dim
        prediction = []
        for i in data:
            prediction.append(np.random.choice(2, size))
        return prediction
