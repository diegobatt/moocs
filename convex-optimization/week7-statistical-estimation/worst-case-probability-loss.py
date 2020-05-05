import numpy as np
import cvxpy as cp

import matplotlib.pyplot as plt


plt.style.use("seaborn")


# Variables
N = 100
mu1, mu2 = 8, 20
sigma1, sigma2 = 6, 17.5
rho = -0.25
risks = np.linspace(-30, 70, N)
total_return = np.array([[r1 + r2 for r2 in risks] for r1 in risks])
products = np.array([[r1 * r2 for r2 in risks] for r1 in risks])

# Marginals distributions
p1 = np.exp(-(risks - mu1)**2 / (2 * sigma1**2))
p1 /= np.sum(p1)
p2 = np.exp(-(risks - mu2)**2 / (2 * sigma2**2))
p2 /= np.sum(p2)

# Optimization problem
joint = cp.Variable((N, N))
objective = cp.Maximize(cp.sum(joint[total_return <= 0]))
constraints = [
    joint >= 0,
    cp.sum(joint, axis=1) == p1,
    cp.sum(joint, axis=0) == p2,
    cp.sum(cp.multiply(joint, products)) - mu1 * mu2 == rho * sigma1 * sigma2
    ]
problem = cp.Problem(objective, constraints)
problem.solve()

print(f"The larger p_loss es given by: {problem.value}")

# Plot the results
R1, R2 = np.meshgrid(risks, risks)
plt.figure(figsize=(12, 7))
plt.contour(R1, R2, np.clip(joint.value, 0, None) , levels=25, cmap="viridis")
plt.colorbar()
plt.show()
