from .util import backend_handler_new
from .common import header
from .common import desc

class RPM(desc):
        
    def __init__(self, params):
        try:
            super().__init__()
            self.username = params['username']
            self.password = params['password']
            self.env_name = '3-RPM'
            self.test_name = ''
            
            self.header = header(env_name="rpm", 
                                 input_dim=24, 
                                 output_dim=3,
                                 info="",
                                 rl=False)
            self.backend = backend_handler_new(username, password, self.test_name, self.env_name)
        except Exception as inst:
            print(inst)
        
    def get_header(self):
        return self.header
        
    def get_test(self):
        return self.backend.get_test('3_RPM_gen_test', 750)
    
    def get_train(self):
        return self.backend.get_train(750, '3_RPM_gen_train')
        
    def submit(self, data):
        return self.backend.submit(data, '3_RPM_evaluate')

