import numpy as np
import cvxpy as cp

import matplotlib.pyplot as plt


plt.style.use("seaborn")

preferences = np.genfromtxt("../storage/preferences-data.csv", dtype=int)
n = 50
m = 1000
rank = cp.Variable(n)
errors = []
for i, j in preferences:
    errors.append(cp.pos(rank[j-1] + 1 - rank[i-1]))
errors = cp.vstack(errors)

cp.Problem(cp.Minimize(cp.sum(errors))).solve()
e_l1 = errors.value.flatten()
cp.Problem(cp.Minimize(cp.norm(errors))).solve()
e_l2 = errors.value.flatten()

print(f"L1 have {np.sum(e_l1 > 1e-4)} non-zero while L2 has {np.sum(e_l2 > 1e-4)}")

plt.figure()
plt.hist(e_l1, bins=30, range=(0, 8), label="L1")
plt.hist(e_l2, alpha=0.5, bins=40, range=(0, 8), label="L2")
plt.legend()
plt.title("Histogram of errors")
plt.show()
