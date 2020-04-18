import numpy as np
import cvxpy as cp


n = 100
m = 300
nts = 100

"""
This data came from matlab. I was reluctant to use it 
so I just generated the data there and brought it to python.
"""
A = np.genfromtxt(
    '../storage/random-matrix.csv', delimiter=',', skip_footer=1
)
c = np.genfromtxt(
    '../storage/random-matrix.csv', delimiter=',', skip_header=m
)
b = A @ (np.ones(n) / 2)
x = cp.Variable(n)
constraints = [x >= 0, x <= 1, A @ x <= b]

cp.Problem(cp.Minimize(c @ x), constraints).solve()
x_hat = x.value
L = c @ x_hat

bounds = np.empty(nts)
violations = np.empty(nts)
ts = np.linspace(0, 1, nts)
for i, t in enumerate(ts):
    x_ = np.array(list(map(lambda x: 1 if x > t else 0, x_hat)))
    bounds[i] = c @ x_
    violations[i] = np.max(A @ x_ - b)
U = min(bounds[violations < 0])

print(f"Lower bound: {L}, Truncated problem value: {U}, diff: {U - L}")



