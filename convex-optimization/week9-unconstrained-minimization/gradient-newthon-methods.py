import numpy as np

from solver import GradientDescent, NewtonRaphson

n = 2
A = np.array([[1, 2], [3, 1]])
x0 = np.array([0, 0])

def f(x):
    aux1 = 1 - A @ x
    aux2 = 1 - x**2
    if any(aux1 <= 0) or any(aux2 <= 0):
        return np.inf
    else:
        return -np.sum(np.log(aux1)) - np.sum(np.log(aux2))

def grad(x):
    return (
        np.sum((A.T / (1 - A @ x)).T, axis=0)
        + 2 * x / (1 - x**2)
    )

solver = GradientDescent(f, grad)
solver.solve(x0, alpha=0.0001, plot=True)

