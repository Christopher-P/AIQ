# Used to clean cartpole data
import numpy as np
import copy

# Load from save
x = np.load('cart_x.npy')
y = np.load('cart_y.npy')

# Convert back to list
x_tmp = []
for i in x:
    a = i[15:16][0][15:17]
    b = i[16:17][0][15:17]
    c = np.concatenate((a, b), axis=0)
    x_tmp.append(c)

x = np.asarray(x_tmp)

min_cart = np.amin(x)
max_cart = np.amax(x)
x = np.divide(np.subtract(x, min_cart), (max_cart - min_cart))

x_tmp = []
for i in x:
    a = np.zeros((32, 32))
    a[15][15] = i[0]
    a[15][16] = i[1]
    a[16][15] = i[2]
    a[16][16] = i[3]
    x_tmp.append(a)

x = np.asarray(x_tmp)

with open('cart_x_2.npy', 'wb') as f:
    np.save(f, x)

print(len(np.unique(x)))
print(len(x))
