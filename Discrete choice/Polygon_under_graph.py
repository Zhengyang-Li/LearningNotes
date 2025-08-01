import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.stats import norm

def polygon_under_graph(x, y, z):
     return [(x[0], y[0], 0.), *zip(x, y, z), (x[-1], y[-1], 0.)]

x = np.linspace(-1, 1, 200)
z = norm.pdf(x, loc=0.5, scale=0.3)
verts = [polygon_under_graph(x, x, z)]
print(verts)
fig = plt.figure()
ax = Axes3D(fig)
poly = Poly3DCollection(verts, alpha=.7)
ax.add_collection3d(poly, zdir='y')
plt.show()
