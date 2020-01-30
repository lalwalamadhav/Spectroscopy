

import pandas as pd
import matplotlib.pyplot as plt
import re
from mpl_toolkits import mplot3d
file = input("Enter (csv) file name:\n")
a = pd.read_csv(file)
b = input("Enter the graph parameters:\n")
#Example: u-i,i-z,z-g
c = re.split("-|,",b)
labels = re.split(",",b)
g = a[c[0]].values.astype(float)
r = a[c[1]].values.astype(float)
i = a[c[2]].values.astype(float)
z = a[c[3]].values.astype(float)
if len(c)==4:
    plt.scatter(g-r,i-z,color='black',s=1)
else:
    ax = plt.axes(projection='3d')
    t = a[c[4]].values.astype(float)
    p = a[c[5]].values.astype(float)
    ax.scatter3D(g-r, i-z, t-p, color='black',s=1)
    ax.set_zlabel(labels[2])
plt.xlabel(labels[0])
plt.ylabel(labels[1])
plt.title("color-color diagram")
plt.show()







