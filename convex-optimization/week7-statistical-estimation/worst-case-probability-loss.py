import numpy as np
import cvxpy as cp

N = 100
mu1, mu2 = 8, 20
sigma1, sigma2 = 6, 17.5
rho = -0.25
risks = np.linspace(-30, 70, N)
total_return = np.array([[r1 + r2 for r2 in risks] for r1 in risks])
products = np.array([[r1 * r2 for r2 in risks] for r1 in risks])

p1 = np.exp(-(risks - mu1)**2 / (2 * sigma1**2))
p1 /= np.sum(p1)
p2 = np.exp(-(risks - mu2)**2 / (2 * sigma2**2))
p2 /= np.sum(p2)

joint = cp.Variable((N, N))
objective = cp.Maximize(cp.sum(joint[total_return <= 0]))
constraints = [
    joint >= 0,
    cp.sum(joint, axis=1) == p1,
    cp.sum(joint, axis=0) == p2,
    cp.sum(cp.multiply())]

problem = cp.Problem(objective, constraints)