# Implemention of random agent
import numpy as np

class R_Agent():

    def __init__(self):
        return None

    # Called for RL type tests
    def act(self, header, data):
        if header.info == 'ViZDoom simulator':
            return np.random.choice(2, header.input_dim)
        else:
            size = header.output_dim
            return np.random.choice(header.num_classes, 1)[0]
    
    # Called for DS type tests
    def predict(self, header, data):
        size = header.output_dim
        prediction = []
        for i in data:
            prediction.append(np.random.choice(2, size))
        return prediction
