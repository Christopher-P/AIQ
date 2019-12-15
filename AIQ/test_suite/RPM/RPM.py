from .common import header, desc

class RPM(desc):
        
    def __init__(self, params):
        try:
            super().__init__()
            self.env_name = '3-RPM'
            self.header = header(env_name="rpm", 
                                 input_dim=24, 
                                 output_dim=3,
                                 info="",
                                 rl=False)
            self.backend = backend
            #TODO: maybe think of way to make this more dynamic??
            self.amount = 750
            self.train = None
            self.test  = None
            self.download_data()

        except Exception as inst:
            print(inst)

    def download_data(self):
        data = {'env':'3_RPM', 'option':'train', 'amt':self.amount}
        self.train = self.backend.submit(data)
        #TODO: Clean train data
        data = {'env':'3_RPM', 'option':'test'}
        self.test = self.backend.submit(data)
        #TODO: Clean test data
        
    def get_header(self):
        return self.header
        
    def get_test(self):
        return self.test
    
    def get_train(self):
        return self.train
        
    def evaluate(self, data):
        data = {'env':'3_RPM', 'option':'evaluate', 'sol':data}
        l = self.backend.submit(data)
        print(l)
        return l

