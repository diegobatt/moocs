import numpy as np
import cvxpy as cp

n = 20  # dimension of x's
M = 25  # number of non-censored data points
K = 100  # total number of points
path = "../storage/censored-data.csv"

X = np.genfromtxt(path, max_rows=n)
c = np.genfromtxt(path, skip_header=n, max_rows=1)
noise = np.genfromtxt(path, skip_header=n+1, max_rows=1)
y = X.T @ c + 0.1 * np.sqrt(n) * noise

idx = sorted(np.arange(K), key=lambda i: y[i])
y = y[idx]
X = X[:, idx]
D = (y[M - 1] + y[M]) /2
y_trunc = y[:M]
y_censored = np.append(y_trunc, D * np.ones(K - M))


def score(c_):
    return np.linalg.norm(c - c_.value) / np.linalg.norm(c)


c_ = cp.Variable(n)
# Ignoring all censored elements
cp.Problem(cp.Minimize(cp.norm(X[:, :M].T @ c_ - y_trunc))).solve()
partial_c_ = c_.value.copy()
print("Ignoring the censored elements, we get: ", score(c_))

# Ignoring the fact that there is censored data
cp.Problem(cp.Minimize(cp.norm(X.T @ c_ - y_censored))).solve()
print("Ignoring the fact that there is censored data, we get: ", score(c_))

# For censored data
# We introduce dummy variables
z = cp.Variable(K-M)
cp.Problem(
    cp.Minimize(
        cp.norm(X[:, :M].T @ c_ - y_trunc)
        + cp.norm(X[:, M:].T @ c_ - z)
    ),
   [z >= D]
).solve()
print("Beign smart about the censored data get us: ", score(c_))

# Getting the lower bound to see how close we got
cp.Problem(cp.Minimize(cp.norm(X.T @ c_ - y))).solve()
print("The best possible score would be: ", score(c_))
