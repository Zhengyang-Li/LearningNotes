import numpy as np
from scipy.stats import gumbel_r
import matplotlib.pyplot as plt


'''
Define 2 Gumbel variables with same scale
'''
'''PDF'''
U_scale = 1
U1_mode = 2
U2_mode = 3

U1 = gumbel_r(loc=U1_mode, scale=U_scale)
U2 = gumbel_r(loc=U2_mode, scale=U_scale)

'''The xaxis and yaxis'''
x = np.linspace(U1.ppf(0.0001), U1.ppf(0.99), 100)
xaxis, yaxis = np.meshgrid(x, x)

'''Assuming U1 and U2 are independent, then the joint distribution of U1 and U2 is'''
z = U1.pdf(xaxis) * U2.pdf(yaxis)

'''3D surface'''
fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
ax.plot_surface(xaxis, yaxis, z, alpha = 0.5, color='blue', zorder = 1)

'''Line'''
line1 = [x, x, U1.pdf(x) * U2.pdf(x)]
line2 = [x, x, np.zeros(np.shape(x))]
ax.plot3D(*line1, 'r-', zorder=0)
ax.plot3D(*line2, 'r-', zorder=0)

'''Cuttng plane'''
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def polygon_under_graph(x, y, z):
    return [(x[0], y[0], 0.), *zip(x, y, z), (x[-1], y[-1], 0.)]

verts = [polygon_under_graph(x, x, U1.pdf(x) * U2.pdf(x))]
poly = Poly3DCollection(verts, facecolors='r', alpha=.5, zorder=0)
ax.add_collection3d(poly, zdir='y')

ax.view_init(30, 30)
ax.text(5, 5, 0.01, 'Choosing alternative 2', zdir=(1,0,1), color='r')
ax.set_xlabel("U1~Gumbel (2,1)")
ax.set_ylabel("U2~Gumbel (3,1)")
ax.set_zlabel("Joint PDF")
plt.savefig('Output\\3D_joint_PDF.png', dpi=600)
plt.show()





'''CDF'''
z = U1.cdf(xaxis) * U2.cdf(yaxis)

'''3D surface'''
fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
ax.plot_surface(xaxis, yaxis, z, alpha = 0.5, color='blue', zorder = 1)
ax.set_xlabel("U1~Gumbel (2,1)")
ax.set_ylabel("U2~Gumbel (3,1)")
ax.set_zlabel("Joint CDF")
plt.savefig('Output\\3D_joint_CDF.png', dpi=600)
plt.show()






'''Difference of two alternatives and the choosing probability'''
U_scale = 1
U1 = np.linspace(0, 10, 100)
U2 = np.linspace(0, 10, 100)
xaxis, yaxis = np.meshgrid(U1, U2)

prob_U1 = np.exp(U_scale * xaxis) / (np.exp(U_scale * xaxis) + np.exp(U_scale * yaxis))

'''3D surface'''
fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
ax.plot_surface(xaxis, yaxis, prob_U1, alpha = 1, cmap=plt.cm.YlGnBu_r, zorder = 0)

'''Line'''
line = [U1, U1, 0.5*np.ones(np.shape(U1))]
ax.plot3D(*line, 'r-', lw=2, zorder=-1)


ax.view_init(30, 210)
ax.set_xlabel("Utility of A1")
ax.set_ylabel("Utility of A2")
ax.set_zlabel("Probability of choosing A1")
plt.savefig('Output\\3D_choosing_probability.pdf', dpi=600, bbox_inches='tight')
plt.show()