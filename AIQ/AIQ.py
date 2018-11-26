from .backend import backend_handler_new

class AIQ():

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.backend = backend_handler_new(self.username, self.password)

        self.agent = None
        self.test_suite = []

    # Check connection
    def connect(self):
        return self.backend.connect()

    # Add a test to the test suite
    def add(self, env_name):
        print("TODO")

    # Evaluate test suite and given agent
    def evaluate(self, ):
        if self.agent == None:
            print("No agent defiend")
        if len(self.test_suite) == 0:
            print("No tests defined")
        print("TODO")

    # Send results to AIQ website
    def submit(self):
        return self.backend.submit(self.results)
        
