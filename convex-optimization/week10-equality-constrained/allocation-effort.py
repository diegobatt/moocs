import numpy as np
import cvxpy as cp

n = 10
m = 20
B = m / 2
edges = np.array([
    [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 7, 8, 9],
    [2, 3, 4, 6, 3, 4, 5, 6, 6, 7, 8, 7, 7, 8, 8, 9, 9, 10, 10, 10]
]) - 1
A = np.zeros((n, m))
for i in range(m):
    A[edges[0, i], i] = -1
    A[edges[1, i], i] = 1

# Data generated with Matlab
a = np.array([
    0.4623, 1.2137, 0.9720, 1.7826, 1.5242, 0.9129, 0.0370,
    1.6428, 0.8894, 1.2309, 1.5839, 1.8436, 1.4764, 0.3525,
    0.8114, 1.8709, 1.8338, 0.8205, 1.7873, 0.1158
])
x_max = np.array([
    1.3529, 1.8132, 1.0099, 1.1389, 1.2028, 1.1987, 1.6038,
    1.2722, 1.1988, 1.0153, 1.7468, 1.4451, 1.9318, 1.4660,
    1.4186, 1.8462, 1.5252, 1.2026, 1.6721, 1.8381
])

z = cp.Variable(n) # Log P
x = cp.Variable(m)
objective = cp.Minimize(z[-1])
st = [
    cp.sum(x) <= B,
    x >= 0, 
    x <= x_max,
    A.T @ z >= -cp.multiply(a, x),
    z[0] == 0
]
problem = cp.Problem(objective, st)
problem.solve()
print("Optimal value Pn: ", np.exp(z[-1].value))

unif_x = B / m * np.ones(m)
st = [
    A.T @ z >= -cp.multiply(a, unif_x),
    z[0] == 0
]
problem = cp.Problem(objective, st)
problem.solve()
print("Pn for uniform allocation: ", np.exp(z[-1].value))