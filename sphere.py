import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg

# Load the image
image = mpimg.imread('screenshot.png')

# Create a sphere
phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0*np.pi:100j]
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Create spherical mapping coordinates for the image
u = np.linspace(0, 1, image.shape[1])
v = np.linspace(0, 1, image.shape[0])
u, v = np.meshgrid(u, v)

# Plot the sphere
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, rstride=5, cstride=5, facecolors=plt.cm.viridis(v), alpha=0.6, zorder=0)

# Map the image onto the sphere
ax.plot_surface(x, y, z, rstride=5, cstride=5, facecolors=plt.cm.viridis(v), shade=False)

# Display the plot
plt.show()
