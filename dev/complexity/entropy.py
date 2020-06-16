import random
import matplotlib.pyplot as plt
import numpy as np

from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.morphology import disk

from test_loader import Loader

###Will run main code
tl      = Loader()
tl.m    = tl.load_mnist()
tl.fm   = tl.load_fmnist()
tl.c10  = tl.load_cifar10()
tl.c100 = tl.load_cifar100()
tl.cart = tl.load_cartpole()

data = [tl.m, tl.fm, tl.c10, tl.c100, tl.cart]

for A in data:
    A_part = A[0]
    A_part = np.reshape(A_part, (len(A_part),32,32))
    s_A = 0.0

    for ind, val in enumerate(A_part):
        entr_img  = entropy(val, disk(1))
        s_A += np.mean(entr_img)

    print(s_A)
exit()

for j in range(0,21):
    
    s_A = 0.0
    s_B = 0.0

    B = tl.add_noise(A, j*5)
    B_part = B[0]
    B_part = np.reshape(B_part, (50000,32,32))

    r_sample = random.sample(range(0, 50000), 1000)



    #print(s_A/1000.0)
    #print(s_B/1000.0)

    print(str(s_A/s_B) + ',')
