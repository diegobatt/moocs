import numpy as np
import time


iters = 30
# Constants definitions
n = 5000
m = 30
sqrt_Q = np.random.normal(10, 2, size=(m, m))
Q = sqrt_Q @ sqrt_Q.T
F = np.random.normal(20, 2, size=(n, m))
D = np.diag(np.random.normal(5, 1, size=n))
E = F @ Q @ F.T + D
mu = np.random.normal(5, 1, size=n)
h = 1

def cost(w):
    return mu @ w - h/2 * w.T @ E @ w

# Solving as dense
b = np.append(mu, 1)
A = np.vstack([E, np.ones(n)])
A = np.hstack([A, np.append(np.ones(n), 0)[:, None]])

times = []
start = time.time()
for _ in range(iters):
    x = np.linalg.solve(A, b)
    w = x[:-1]
    end = time.time()
    times.append(end-start)
    start = end

print(f"Took {np.mean(times)} of the stupid way to get {cost(w)}")

# Solving smartly
ones_n = np.ones((n, 1))
zeros_m = np.zeros((m, 1))
zeros_nm = np.zeros((n, m))
I = np.identity(m)

times = []
start = time.time()
for _ in range(iters):
    inv_A_11 = np.block(
        [[np.diag(1 / np.diagonal(D)), zeros_nm],
        [zeros_nm.T, np.linalg.inv(Q)]]
    )
    A_12 = np.block([[ones_n, F], [zeros_m, -I]])
    A_21 = A_12.T
    b_1 = np.append(mu, zeros_m.flatten())
    b_2 = np.append(1, zeros_m.flatten())
    A_21_inv_11 = A_21 @ inv_A_11
    x_2 = np.linalg.solve(-A_21_inv_11 @ A_12, b_2 - A_21_inv_11 @ b_1)
    x_1 = inv_A_11 @ (b_1 - A_12 @ x_2)
    w = x_1[:n]
    end = time.time()
    times.append(end-start)
    start = end

print(f"Took {np.mean(times)} of the smart way to get {cost(w)}")
