import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

plt.style.use("seaborn")

x = np.genfromtxt("../storage/sphere-fit.csv")
plt.figure()
plt.scatter(x[:, 0], x[:, 1])
plt.show()

# find the center
c = cp.Variable(2)
cs = cp.vstack([c for _ in range(len(x))])
objective = cp.Minimize(cp.norm(x - cs))
cp.Problem(objective).solve()
c_ = c.value

# find the radius
rho = cp.Variable(nonneg=True)
x_ = rho * ((x - c_) / np.linalg.norm(x - c_, axis=1)[:, None]) + cs.value
objective = cp.Minimize(cp.norm(x_ - x))
problem = cp.Problem(objective)
problem.solve()

plt.figure()
plt.scatter(x_.value[:, 0], x_.value[:, 1])
plt.scatter(x[:, 0], x[:, 1])
plt.show()