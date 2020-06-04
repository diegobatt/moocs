import numpy as np

from solver import GradientDescent, NewtonRaphson

n = 500
m = 500
A = np.random.normal(2, 1, size=(m, n))
x0 = np.zeros(n)

def f(x):
    aux1 = 1 - A @ x
    aux2 = 1 - x**2
    if any(aux1 <= 0) or any(aux2 <= 0):
        return np.inf
    else:
        return -np.sum(np.log(aux1)) - np.sum(np.log(aux2))

def grad(x):
    return A.T @ (1 / (1 - A @ x)) + 2 * x / (1 - x**2)

def hessian(x):
    W = np.diag((1 / (1 - A @ x))**2)
    V = np.diag(2 / (1 - x**2) + 4 * x**2 / (1 - x**2)**2)
    return A.T @ W @ A + V


gd = GradientDescent(f, grad)
gd.solve(x0, alpha=0.001, plot=True)
nr = NewtonRaphson(f, grad, hessian)
nr.solve(x0, threshold=0.00001, alpha=0.001, plot=True)

