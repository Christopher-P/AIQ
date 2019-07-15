import numpy as np
import csv
import os
class T():
    
    def __init__(self, out):
        self.out = out

    def sample(self):
        # folded distribution
        return abs(np.random.normal()) / self.out

# create a hundred tests of increasing difficulty
tests = []

for i in range(1,10):
    tests.append(T(i))

for i in range(50,52):
    tests.append(T(i))

for i in range(100,101):
    tests.append(T(i))

os.remove("fake.csv")

for i in range(len(tests)):
    for j in range(len(tests)):
        A = tests[i].sample()
        B = tests[j].sample()
        if A < B:
            x = 0.8
            y = 0.2
        if A > B:
            x = 0.2
            y = 0.8

        C = (x*tests[i].sample() + y*tests[j].sample()) / 2.0



        with open('fake.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            spamwriter.writerow(('D' + str(i), 0.0, A))
            spamwriter.writerow(('D' + str(j), 0.0, B))
            spamwriter.writerow(('D' + str(i) + '=' + 'D' + str(j), 0.0, C))
