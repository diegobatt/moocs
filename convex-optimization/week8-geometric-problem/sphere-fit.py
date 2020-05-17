import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

plt.style.use("seaborn")

x = np.genfromtxt("../storage/sphere-fit.csv")
plt.figure()
plt.scatter(x[:, 0], x[:, 1])
plt.show()

# Problem is an LP expressed like this
x_norms = cp.norm(x, axis=1) ** 2
c = cp.Variable(2)
rho = cp.Variable()
objective = cp.Minimize(cp.norm(x_norms - x @ c - rho))
cp.Problem(objective).solve()
# Retrieve the center and radius with simple transformations
center = 1/2 * c.value
radius = np.sqrt(rho.value + center @ center)
x_ = radius * (x - center) / np.linalg.norm(x - center, axis=1)[:, None] + center

# Plot results
plt.figure()
plt.scatter(x[:, 0], x[:, 1])
plt.scatter(x_[:, 0], x_[:, 1])
plt.show()