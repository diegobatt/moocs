import numpy as np
import cvxpy as cp

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

plt.style.use("seaborn")

# Instance data
x = np.array([
    [3.5674, 4.1253, 2.8535, 5.1892, 4.3273, 3.8133, 3.4117,
    3.8636, 5.0668, 3.9044, 4.2944, 4.7143, 3.3082, 5.2540,
    2.5590, 3.6001, 4.8156, 5.2902, 5.1908, 3.9802],
    [-2.9981, 0.5178, 2.1436, -0.0677, 0.3144, 1.3064, 3.9297,
    0.2051, 0.1067, -1.4982, -2.4051, 2.9224, 1.5444, -2.8687,
    1.0281, 1.2420, 1.2814, 1.2035, -2.1644, -0.2821]
])
y = np.array([
    [-4.5665, -3.6904, -3.2881, -1.6491, -5.4731, -3.6170, -1.1876,
    -1.0539, -1.3915, -2.0312, -1.9999, -0.2480, -1.3149, -0.8305,
    -1.9355, -1.0898, -2.6040, -4.3602, -1.8105, 0.3096],
    [2.4117, 4.2642, 2.8460, 0.5250, 1.9053, 2.9831, 4.7079,
    0.9702, 0.3854, 1.9228, 1.4914, -0.9984, 3.4330, 2.9246,
    3.0833, 1.5910, 1.5266, 1.6256, 2.5037, 1.4384]
])
z = np.array([
    [1.7451, 2.6345, 0.5937, -2.8217, 3.0304, 1.0917, -1.7793,
    1.2422, 2.1873, -2.3008, -3.3258, 2.7617, 0.9166, 0.0601,
    -2.6520, -3.3205, 4.1229, -3.4085, -3.1594, -0.7311],
    [-3.2010, -4.9921, -3.7621, -4.7420, -4.1315, -3.9120, -4.5596,
    -4.9499, -3.4310, -4.2656, -6.2023, -4.5186, -3.7659, -5.0039,
    -4.3744, -5.0559, -3.9443, -4.0412, -5.3493, -3.0465]
])

# Solving the problem
a_x, b_x = cp.Variable(2), cp.Variable()
a_y, b_y = cp.Variable(2), cp.Variable()
a_z, b_z = cp.Variable(2), cp.Variable()
objective = cp.Minimize(cp.norm(a_x) + cp.norm(a_y) + cp.norm(a_z))
constraints = [
    (a_x @ x + b_x) - (a_y @ x + b_y) >= 1,
    (a_x @ x + b_x) - (a_z @ x + b_z) >= 1,
    (a_y @ y + b_y) - (a_x @ y + b_x) >= 1,
    (a_y @ y + b_y) - (a_z @ y + b_z) >= 1,
    (a_z @ z + b_z) - (a_x @ z + b_x) >= 1,
    (a_z @ z + b_z) - (a_y @ z + b_y) >= 1
]
problem = cp.Problem(objective, constraints)
problem.solve()

# Plotting
d1 = np.linspace(
    np.min([x[0], y[0], z[0]]) - 1, np.max([x[0], y[0], z[0]]) + 1, 150
)
d2 = np.linspace(
    np.min([x[1], y[1], z[1]]) - 1, np.max([x[1], y[1], z[1]]) + 1, 150
)
dd1, dd2 = np.meshgrid(d1, d2)
dd3 = np.zeros(dd1.shape)
for i in range(dd1.shape[0]):
    for j in range(dd1.shape[1]):
        val = np.array([dd1[i, j], dd2[i, j]])
        if (
            (a_x.value @ val + b_x.value) > (a_y.value @ val + b_y.value)
            and (a_x.value @ val + b_x.value) > (a_z.value @ val + b_z.value)
        ):
            dd3[i, j] = 1
        elif (
            (a_y.value @ val + b_y.value) > (a_x.value @ val + b_x.value)
            and (a_y.value @ val + b_y.value) > (a_z.value @ val + b_z.value)
        ):
            dd3[i, j] = 2
        else:
            dd3[i, j] = 3

plt.figure(figsize=(10, 5))
plt.title("Decision boundaries")
plt.pcolor(
    dd1, dd2, dd3,
    cmap=ListedColormap(["blue", "green", "red"]),
    alpha=0.2,
    snap=True
)
plt.scatter(*x)
plt.scatter(*y)
plt.scatter(*z)
plt.show()       
