from test_loader import Loader

import random

import matplotlib.pyplot as plt
import numpy as np

from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.morphology import disk


# Load data
tl    = Loader()
tl.fm = tl.load_fmnist()

A = tl.fm
A_part = A[0]
A_part = np.reshape(A_part, (50000,32,32))

for j in range(0,21):
    
    s_A = 0.0
    s_B = 0.0

    B = tl.add_noise(A, j*5)
    B_part = B[0]
    B_part = np.reshape(B_part, (50000,32,32))

    r_sample = random.sample(range(0, 50000), 1000)

    for ind, val in enumerate(r_sample):

        entr_img  = entropy(A_part[val], disk(1))
        entr_img2 = entropy(B_part[val], disk(1))

        s_A += np.mean(entr_img)
        s_B += np.mean(entr_img2)

    #print(s_A/1000.0)
    #print(s_B/1000.0)

    print(str(s_A/s_B) + ',')






