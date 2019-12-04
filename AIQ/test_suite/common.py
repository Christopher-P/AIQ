# Universal super class
class desc():
    
    def __init__(self):
        # Initial setup
        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = None
        self.results = []
        self.info = None
        self.init = False
    

class header():
    
    def __init__(self, env_name, input_dim, output_dim, 
                info, rl, num_classes=1, env_min_score=0.0, 
                env_max_score=1.0):
        self.env_name = env_name
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_classes = num_classes
        self.info = info
        self.rl = rl
        self.env_min_score = env_min_score
        self.env_max_score = env_max_score

    
    
