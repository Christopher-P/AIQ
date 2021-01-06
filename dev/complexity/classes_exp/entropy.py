import random
import math

import matplotlib.pyplot as plt
import numpy as np

from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.morphology import disk

from test_loader import Loader

# Will run main code
tl = Loader()
classes = np.arange(10, 110, step=10)
print(classes)
entropy_list = []

for num in classes:
    # A is dataset
    A = tl.load_cifar100(classes=num)
    A_part = A[0]
    length = A[2][2].shape[0]
    A_part = np.reshape(A_part, (len(A_part), 32, 32))
    s_A = 0.0

    mml =  math.log(length, 2)

    for ind, val in enumerate(A_part):
        if ind % 1000 == 0:
            print(ind)
        entr_img  = entropy(val, disk(1))
        s_A = s_A + np.mean(entr_img) + mml

    s_A = s_A / len(A_part)

    print(s_A)
    entropy_list.append(s_A)

print(entropy_list)
exit()
