import itertools as it
from pprint import pprint

import cvxpy as cp
import numpy as np

x = cp.Variable((2, 1))
Q = np.array([[1, -0.5], [-0.5, 2]])
c = np.array([-1, 0])
u = np.array([[-2, -3, 5]])
A = np.array([[1, 2], [1, -4], [-1, -1]])
constraints = [A @ x <= u.T]
obj = cp.Minimize(cp.quad_form(x, Q) + c.T @ x)

# First problem
optimal = cp.Problem(obj, constraints).solve()
duals = constraints[0].dual_value
print("Optimal x: ", x.value)
print("Dual variables: ", duals)

# Perturbation analysis
perturbs = [-0.1, 0, 0.1]
combs = it.product(perturbs, perturbs, [0])
results = {}

for perturb in combs:
    b = u + np.array(perturb)
    guess = optimal - (duals.T @ perturb)[0]
    solution = cp.Problem(obj, [A @ x <= b.T]).solve()
    results[(perturb[0], perturb[1])] = (solution, guess, solution - guess)

print("Results for different perturbations: ")
pprint(results)
print("Perturbations order by delta guess")
pprint(sorted([(k, v[2]) for k, v in results.items()], key=lambda x: x[1]))
