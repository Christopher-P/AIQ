from .util import AIQ
from .util import Header
from .connection import backend_handler

class RPM(AIQ):
        
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        
        self.header = Header('3-RPM', 3*8, 3*1, '3-rpm test')

        self.backend = backend_handler(username, password)
        
    def get_header(self):
        return self.header
        
    def get_test(self):
        return self.backend.get_test('3_RPM_gen_test')
    
    def get_train(self, amt):
        return self.backend.get_train(amt, '3_RPM_gen_train')
        
    def submit(self, data):
        return self.backend.submit(data, '3_RPM_evaluate')
    
    def connect(self):
        return self.backend.connect()
    
       
        

'''        
class RPM_exe(AIQ):

    def __init__(self):        
        from subprocess import Popen, PIPE
        self.p = Popen(['AIQ_Front.exe'], shell=True, stdout=PIPE, stdin=PIPE)
        
    def get_train(self, amt):
        value = str(amt) + '\n'
        value = bytes(value, 'UTF-8')  # Needed in Python 3.
        self.p.stdin.write(value)
        self.p.stdin.flush()
        result = self.p.stdout.readline().strip()
        print(result)
            
    def get_test(self):
        value = bytes(amt, 'UTF-8')  # Needed in Python 3.
        p.stdin.write(value)
        p.stdin.flush()
        result = p.stdout.readline().strip()
        print(result)
            
    def submit(self, solution):
        value = bytes(amt, 'UTF-8')  # Needed in Python 3.
        p.stdin.write(value)
        p.stdin.flush()
        result = p.stdout.readline().strip()
        print(result)
        
    def connect(self):
        return super().connect()
        
'''
