import numpy as np
import cvxpy as cp

# Retrieve data
path = "../storage/max-volume-rectangle.csv"
A = np.genfromtxt(path, skip_footer=1, delimiter=" ")
b = np.genfromtxt(path, skip_header=len(A), delimiter=" ")

# Problem definition
lower = cp.Variable(n)
upper = cp.Variable(n)
sides = upper - lower
volume = cp.prod(sides)
objective = cp.Maximize(cp.geo_mean(sides))
constraints = [
    sides >= 0,
    A @ lower <= b,
    A @ upper <= b
]
problem = cp.Problem(objective, constraints)
problem.solve()
volume.value