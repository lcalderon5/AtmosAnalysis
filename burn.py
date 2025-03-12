import numpy as np
import matplotlib.pyplot as plt

# Plot simple function

def f(x, y):
    a = 1
    b = 1
    c = 1

    D = b - c*x/y**2

    return  a / (b - D)

def g(z, y):
    a = 1
    b = 1
    c = 1

    x = (- a / z * + b) / c * y**2

    return x


# Create a grid of x and y values
x = np.linspace(0, 10, 400)
y = np.linspace(0, 10, 400)

X, Y = np.meshgrid(x, y)
Z = g(X, Y)

# Remove negative Z values
Z = np.maximum(Z, 0)

# Create a surface plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
# Log scale for z-axis
ax.set_zscale('log') 
ax.set_title('Surface plot of f(x, y)')

plt.show()

# Create a contour plot
plt.figure()
plt.contourf(X, Y, Z, levels=100)
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Contour plot of f(x, y)')

plt.show()