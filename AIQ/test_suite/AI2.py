from .common import header
from .common import desc
import json
import jsonlines

class AI2(desc):

    def __init__(self):
        try:
            # Gives common variables to all environments
            super().__init__()

            # Define header
            self.header = header(env_name="AllenInstitute2", 
                                 input_dim=6, 
                                 output_dim=1,
                                 info="https://leaderboard.allenai.org/open_book_qa/submissions/about",
                                 rl=False)

            self.train_X, self.train_Y = self.load_data("../AIQ/test_suite/AI2_data/train_complete.jsonl")
            self.dev_X, self.dev_Y   = self.load_data("../AIQ/test_suite/AI2_data/dev_complete.jsonl")
            self.test_X, self.test_Y  = self.load_data("../AIQ/test_suite/AI2_data/test_complete.jsonl")
        except Exception as inst:
            print(inst)

    def get_header(self):
        return self.header

    def get_train(self):
        return self.train_X, self.train_Y

    def get_dev(self):
        return self.dev_X, self.dev_Y

    def get_test(self):
        return self.test_X

    def evaluate(self, pred):
        score = 0.0
        for ind, val in enumerate(pred):
            if self.test_Y[ind][0] in val:
                score = score + 1.0 / len(val)
        return score / len(self.test_Y)
                

    def load_data(self, path):
        X = []
        Y = []
        with jsonlines.open(path) as reader:
            for obj in reader:
                x = []
                y = []
                x.append(obj['question']['stem'])
                x.append(obj['question']['choices'][0]['text'])
                x.append(obj['question']['choices'][1]['text'])
                x.append(obj['question']['choices'][2]['text'])
                x.append(obj['question']['choices'][3]['text'])
                x.append(obj['fact1'])
                ans = obj['answerKey']
                if ans == "A":
                    y.append(0)
                if ans == "B":
                    y.append(1)
                if ans == "C":
                    y.append(2)
                if ans == "D":
                    y.append(3)
                X.append(x)
                Y.append(y)
        return (X,Y)
