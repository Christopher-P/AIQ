from .util import AIQ
from .Header_def import Header
from AIQ.backend import Backend_DS

class RPM(AIQ):
        
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        
        self.header = Header('3-RPM', 3*8, 3*1, '3-rpm test')

        self.backend = Backend_DS(username, password)
        
    def get_header(self):
        return self.header
        
    def get_test(self, amt):
        return self.backend.get_test('3_RPM_gen_test', amt)
    
    def get_train(self, amt):
        return self.backend.get_train(amt, '3_RPM_gen_train')
        
    def submit(self, data):
        return self.backend.submit(data, '3_RPM_evaluate')
    
    def connect(self):
        return self.backend.connect()
