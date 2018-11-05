import json
import requests
from threading import Thread, Lock

from .util import AIQ


class Benchmark(AIQ):

    def __init__(self, test_names):
        super().__init__()
        
        self.envs = []
        for i in test_names:
            #https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/
            module = __import__('test_suite')
            my_class = getattr(module, i)
            my_class2 = getattr(my_class, i)
            instance = my_class2()
            self.envs.append(instance)
        
    def begin(self):
        for i in range(len(self.envs)):
            self.envs[i].get_header()
    