import numpy as np
import cvxpy as cp
from scipy.stats import bernoulli
from progressbar import progressbar

# Retrieve data
path = "../storage/max-volume-rectangle.csv"
A = np.genfromtxt(path, skip_footer=1, delimiter=" ")
b = np.genfromtxt(path, skip_header=len(A), delimiter=" ")

# Problem definition
n = A.shape[1]
lower = cp.Variable(n)
upper = cp.Variable(n)
sides = upper - lower
volume = cp.prod(sides)
objective = cp.Maximize(cp.geo_mean(sides))
A_u = np.maximum(A, 0)
A_l = np.maximum(-A, 0)
constraints = [
    sides >= 0,
    A_u @ upper - A_l @ lower <= b,
]
problem = cp.Problem(objective, constraints)
problem.solve()
volume.value

# constraints checker
checks = 1000000
print(f"Starting {checks} random corner checks...")
for _ in progressbar(range(checks)):
    mask = bernoulli.rvs(0.5, size=n)
    corner = upper.value * mask + lower.value * (-mask + 1)
    assert all(A @ corner <= b)
print(f"{checks} random corners checks are inside the polyhedron!")
print(f"Final volume {volume.value}")