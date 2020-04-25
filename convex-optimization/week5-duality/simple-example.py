import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt


plt.style.use("seaborn")

# Problem visualization
x = np.linspace(-1, 5, 300)
y = x**2 + 1
constraint = (x - 2)*(x - 4) <= 0
feasible = np.ma.masked_where(constraint, y)
non_feasible = np.ma.masked_where(~constraint, y)

def lagrangian(h, x=x):
    return x**2 + 1 + h * (x - 2)*(x - 4)

plt.figure(figsize=(9, 5))
plt.plot(x, feasible)
plt.plot(x, non_feasible)
plt.plot(x, lagrangian(5), '--')
plt.plot(x, lagrangian(10), '--')
plt.show()

# Dual problem
def dual(h):
    return -9 * h**2 / (h + 1) + 8*h + 1

h = np.linspace(0, 8, 300)
plt.figure(figsize=(9, 5))
plt.plot(h, dual(h))
plt.show()


