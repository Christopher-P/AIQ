from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random

fig = plt.figure()
ax = plt.axes(projection='3d')

# Data for a three-dimensional line
#zline = np.linspace(0, 15, 1000)
#xline = np.sin(zline)
#yline = np.cos(zline)
#ax.plot3D(xline, yline, zline, 'gray')

# Data for three-dimensional scattered points
a = []
b = []
c = []
sim = []

for i in range(8000):
    a.append(random.uniform(0, 1))

a.append(1.0)
a.append(0.00001)

for i in range(len(a)):
    b.append(random.uniform(0, a[i]))

for i in range(len(a)):
    c.append(random.uniform(b[i], a[i]))

for i in range(len(a)):
    num = abs(abs(a[i] - c[i]) - abs(b[i] - c[i]))
    den = abs(a[i] - b[i])
    sim.append(num/den)


### Axis labels
ax.set_xlabel('$A$', fontsize=20)
ax.set_ylabel('$B$', fontsize=20)
ax.yaxis._axinfo['label']['space_factor'] = 3.0
# set z ticks and labels
ax.set_zticks([-1, 0, 1])
# change fontsize
for t in ax.zaxis.get_major_ticks(): t.label.set_fontsize(10)
# disable auto rotation
ax.zaxis.set_rotate_label(False) 
ax.set_zlabel('AB', fontsize=30, rotation = 0)
###

p = ax.scatter3D(a, b, c, c=sim);
v = np.linspace(0.0, 1.0, 11, endpoint=True)
fig.colorbar(p, ticks=v, label='Similarity', orientation='vertical')

plt.show()
exit()
################################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.random.standard_normal(100)
y = np.random.standard_normal(100)
z = np.random.standard_normal(100)
c = np.random.standard_normal(100)

img = ax.scatter(x, y, z, c=c, cmap=plt.hot())
plt.show()

exit()



from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

A = np.linspace(0, 1, 100)
B = np.linspace(0, 1, 100)
AB = np.linspace(0, 1, 100)

sim = []
at  = []
bt  = []
ct  = []

num = np.subtract(np.subtract(A, AB), np.subtract(B, AB))
den = np.subtract(A, B)

for i in range(100):
    if A[i] >= AB[i]:
        if AB[i] >= B[i]:
            at.append(A[i])
            bt.append(B[i])
            ct.append(AB[i])
            
            num = abs(abs(at[-1] - ct[-1]) - abs(bt[-1] - ct[-1]))
            den = abs(at[-1] - bt[-1])

            if den == 0:
                sim.append(-1)
            else:
                sim.append(num / den)

print(len(at), len(bt), len(ct), len(sim))
print(sim)

img = ax.scatter(at, bt, ct, c=sim, cmap=plt.hot())
fig.colorbar(img)
plt.show()
