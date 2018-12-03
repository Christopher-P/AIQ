from .util import AIQ
from .Header_def import Header
from AIQ.backend import backend_handler
from .common import header
from .common import desc

class RPM(AIQ):
        
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.env_name = '3-RPM'
        self.test_name = ''
        
        self.header = Header(self.env_name, 3*8, 3*1, '3-rpm test')

        self.backend = backend_handler(username, password, self.test_name, self.env_name)
        
    def get_header(self):
        return self.header
        
    def get_test(self, amt):
        return self.backend.get_test('3_RPM_gen_test', amt)
    
    def get_train(self, amt):
        return self.backend.get_train(amt, '3_RPM_gen_train')
        
    def submit(self, data):
        return self.backend.submit(data, '3_RPM_evaluate')

