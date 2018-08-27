from .util import AIQ
from .util import Header
from .connection import Backend_DS

class gen(AIQ):
        
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        
        self.header = Header('RPM', 3*8, 3*1, 'rpm test')

        self.backend = Backend_DS(username, password)
        
    def get_header(self):
        return self.header
        
    def get_test(self, n):
        return self.backend.get_test('RPM_gen_test', n)
    
    def get_train(self, amt):
        return self.backend.get_train(amt, 'RPM_gen_train')
        
    def submit(self, data):
        return self.backend.submit(data, 'RPM_evaluate')
    
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